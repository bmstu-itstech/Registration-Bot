import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from redis import asyncio as aioredis

import utils
from custom_types import Questionnaire, AnswerButton, QuestionButton
from micro_services.ApiGateWay import bot_client

# Настроим логирование
logging.basicConfig(level=logging.INFO)


async def run_instance(token, bot_id):
    """
    Функция запускает бота по его токену и ID.
    """

    logging.info(f'Starting bot id{bot_id}...')

    # Подключимся к редису
    redis = aioredis.Redis.from_url(f'redis://localhost:6379/{bot_id}')
    storage = RedisStorage(redis)

    # Инициализируем бота
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    # Инициализируем роутер
    router = Router()
    dp.include_router(router)

    @router.message(CommandStart())
    async def cmd_start(message: Message, state: FSMContext) -> None:
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != Questionnaire.completed and \
                user_status != Questionnaire.in_process and \
                user_status != Questionnaire.on_approval:
            await state.set_state(Questionnaire.in_process)
            await state.update_data(answers=dict(), prev_questions=list(), question_id=1)
            await utils.send_question(state, message.chat.id, bot_id, bot)
        else:
            await message.answer('Вы уже заполнили анкету!')

    @router.message(Command('reset_my_questionnaire_please'))
    async def cmd_reset(message: Message, state: FSMContext) -> None:
        await state.set_state(Questionnaire.in_process)
        await state.update_data(answers=dict(), prev_questions=list(), question_id=1)
        await utils.send_question(state, message.chat.id, bot_id, bot)

    @router.message()
    async def process_text(message: Message, state: FSMContext) -> None:
        """
        Функция обрабатывает текстовые ответы пользователя
        """

        await message.delete()
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != Questionnaire.completed:
            data = await state.get_data()
            # Get next module id
            question_id = data['question_id']
            module = await bot_client.get_question(bot_id, question_id)
            # Если кнопочный вопрос и прилетел текстовый ответ, выдадим просьбу нажать кнопку
            if len(module.buttons) > 0:
                await message.answer('Чтобы ответить, нажмите на одну из кнопок')
                return
            # Удалим предыдущее сообщение бота
            await bot.delete_message(message.chat.id, data['prev_message_id'])
            # Добавим ответ в стейт
            answers = data['answers']
            answers[question_id] = message.text
            # Добавим id вопроса в стейт в качестве предыдущего вопроса
            data['prev_questions'].append(question_id)
            # Загрузим изменения в стейт
            await state.update_data(answers=answers, question_id=module.next_id, prev_questions=data['prev_questions'])

            if module.next_id is not None and \
                    (user_status != Questionnaire.on_approval or
                     str(module.next_id) not in data['on_approval'].keys()):
                # Showing that telegram_bot is typing its module
                await bot.send_chat_action(message.chat.id, 'typing')
                # Send next module
                await utils.send_question(state, message.chat.id, bot_id, bot)
            elif user_status == Questionnaire.on_approval:
                await utils.finish_questionnaire(state, message.chat.id, bot_id, bot, module.next_id)
            else:
                await utils.finish_questionnaire(state, message.chat.id, bot_id, bot)
        # If the user has already passed the questionnaire
        else:
            await message.answer('Вы уже заполнили анкету!')

    @router.callback_query(Text('questionnaire_over'))
    async def process_questionnaire_over(callback_query: CallbackQuery,
                                         state: FSMContext) -> None:
        await callback_query.message.edit_reply_markup()
        answers = (await state.get_data())['answers']
        await bot_client.push_answers(callback_query.message.chat.id, bot_id, answers)
        await state.set_state(Questionnaire.completed)
        await callback_query.answer('Ответы записаны!')
        await bot.send_message(callback_query.message.chat.id, 'Ответы записаны!')

    @router.callback_query(Text('get_back'))
    async def process_get_back(callback_query: CallbackQuery,
                               state: FSMContext) -> None:
        # Удалим сообщение сразу после нажатия пользователя на кнопку
        await callback_query.message.delete()
        data = await state.get_data()
        previous_id = data['prev_questions'].pop()
        data['answers'].pop(data['question_id'], None)
        await state.update_data(prev_questions=data['prev_questions'], answers=data['answers'], question_id=previous_id)
        await utils.send_question(state, callback_query.message.chat.id, bot_id, bot)

    @router.callback_query(QuestionButton.filter())
    async def process_question_callback(callback_query: CallbackQuery,
                                        callback_data: QuestionButton,
                                        state: FSMContext) -> None:
        await callback_query.message.delete()
        data = await state.get_data()
        answers = data['answers']
        # Write answers to temporary storage and reset main storage
        await state.update_data(on_approval=answers, answers=dict(), question_id=callback_data.question_id)
        # Send requested module
        await utils.send_question(state, callback_query.message.chat.id, bot_id, bot)

    @router.callback_query(AnswerButton.filter())
    async def process_answer_callback(callback_query: CallbackQuery,
                                      callback_data: AnswerButton,
                                      state: FSMContext) -> None:
        # Удалим сообщение после ответа пользователя
        await callback_query.message.delete()
        # Getting user state
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != Questionnaire.completed:
            data = await state.get_data()
            # Get answers dict from the state
            answers = data['answers']
            # Get the module id
            question_id = data['question_id']
            # Добавим id вопроса в стейт в качестве предыдущего вопроса
            data['prev_questions'].append(question_id)
            # Write the answer to the state
            answers[question_id] = callback_data.answer
            await state.update_data(answers=answers, prev_questions=data['prev_questions'])

            # If there is next module
            if callback_data.next_id is not None and \
                    (user_status != Questionnaire.on_approval or
                     str(callback_data.next_id) not in data['on_approval'].keys()):
                button_id = int(callback_data.next_id)
                # Showing that telegram_bot is typing its module
                await bot.send_chat_action(callback_query.message.chat.id, 'typing')
                # Send next module based on button ID
                await state.update_data(question_id=button_id)
                await utils.send_question(state, callback_query.message.chat.id, bot_id, bot)
                await callback_query.answer(None)
            elif user_status == Questionnaire.on_approval:
                await utils.finish_questionnaire(state, callback_query.message.chat.id, bot_id,
                                                 bot, callback_data.next_id)
            # If the user passed all the questions
            else:
                await utils.finish_questionnaire(state, callback_query.message.chat.id, bot_id, bot)

        # If the user has already passed the questionnaire
        else:
            await bot.send_message(callback_query.message.chat.id, 'Вы уже заполнили анкету!')

    await dp.start_polling(bot)


async def test():
    from dotenv import load_dotenv
    load_dotenv()
    tasks = [
        run_instance(os.getenv("TEST_TOKEN1"), 1),
        run_instance(os.getenv("TEST_TOKEN2"), 2)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(test())
