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

from telegram_bot import utils
from telegram_bot.custom_types import Questionnaire, AnswerButton, QuestionButton
from micro_services.ApiGateWay import bot_client

# Настроим логирование
logging.basicConfig(level=logging.INFO)


async def run_instance(bot_id):
    """
    Функция запускает бота по его ID.
    """

    logging.info(f'Starting bot id{bot_id}...')

    # Ищем токен бота в БД
    # for bot in bot_status.bots:
    #     print(bot.bot_survey_id, bot.tg_token)
    #     if bot.bot_survey_id == bot_id:
    #         token = bot.tg_token
    bot_status = await bot_client.get_bot(user_id=2, bot_id=bot_id)
    logging.info(f'{bot_status.tg_token}, {bot_status.owner}')
    token = bot_status.tg_token
    # Если не найдено такого бота, прерываем функцию
    if token == "":
        logging.error(f'There is no bot with ID "{bot_id}"!')
        return

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
        # Если пользователь еще не заполнил анкету
        if user_status != Questionnaire.completed and \
                user_status != Questionnaire.in_process and \
                user_status != Questionnaire.on_approval:
            await state.set_state(Questionnaire.in_process)
            await state.update_data(answers=dict(), prev_questions=list(), question_id=1)
            await message.answer(bot_status.start_message)
            await utils.send_question(state, message.chat.id, bot_id, bot)
        elif user_status == Questionnaire.in_process:
            await message.answer('Вы уже в процессе регистрации!')
        elif user_status == Questionnaire.on_approval:
            await message.answer('Вы уже в процессе подтверждения регистрации!')
        else:
            await message.answer('Вы уже прошли регистрацию!')

    @router.message(Command('reset_my_questionnaire_please'))
    async def cmd_reset(message: Message, state: FSMContext) -> None:
        await state.set_state()
        await state.update_data(answers=dict(), prev_questions=list(), question_id=0)
        await message.answer("Состояние сброшено!")

    @router.message()
    async def process_text(message: Message, state: FSMContext) -> None:
        """
        Функция обрабатывает текстовые ответы пользователя
        """

        await message.delete()
        user_status = await state.get_state()
        # Если пользователь еще не заполнил анкету
        if user_status != Questionnaire.completed:
            data = await state.get_data()
            # Получим id модуля
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
                    module.next_id != 0 and \
                    (user_status != Questionnaire.on_approval or
                     str(module.next_id) not in data['on_approval'].keys()):
                await bot.send_chat_action(message.chat.id, 'typing')
                # Отправим следующий модуль
                await utils.send_question(state, message.chat.id, bot_id, bot)
            elif user_status == Questionnaire.on_approval:
                await utils.finish_questionnaire(state, message.chat.id, bot_id, bot, module.next_id)
            else:
                await utils.finish_questionnaire(state, message.chat.id, bot_id, bot)
        # Если пользователь уже прошел анкету
        else:
            await message.answer('Вы уже прошли регистрацию!')

    @router.callback_query(Text('questionnaire_over'))
    async def process_questionnaire_over(callback_query: CallbackQuery,
                                         state: FSMContext) -> None:
        await callback_query.message.edit_reply_markup()
        answers_dict = (await state.get_data())['answers']
        answers_list = await utils.pack_answers(answers_dict)
        response = await bot_client.push_answers(callback_query.message.chat.id, bot_id, answers_list,
                                                 callback_query.from_user.username)
        await state.set_state(Questionnaire.completed)
        await callback_query.answer('Ответы записаны!')
        await bot.send_message(callback_query.message.chat.id, f'Спасибо, путник, за регистрацию.\n'
                                                               f'Ваш уникальный код: {response.code}')

    @router.callback_query(Text('get_back'))
    async def process_get_back(callback_query: CallbackQuery,
                               state: FSMContext) -> None:
        # Удалим сообщение сразу после нажатия пользователя на кнопку
        await callback_query.message.delete()
        data = await state.get_data()
        previous_id = data['prev_questions'].pop()
        data['answers'].pop(data['question_id'], None)
        await state.update_data(prev_questions=data['prev_questions'], answers=data['answers'],
                                question_id=previous_id)
        await utils.send_question(state, callback_query.message.chat.id, bot_id, bot)

    @router.callback_query(QuestionButton.filter())
    async def process_question_callback(callback_query: CallbackQuery,
                                        callback_data: QuestionButton,
                                        state: FSMContext) -> None:
        await callback_query.message.delete()
        data = await state.get_data()
        answers = data['answers']
        # Запишем ответы во временный словарь on_approval и сбросим answers
        await state.update_data(on_approval=answers, answers=dict(), question_id=callback_data.question_id)
        # Отправим запрошенный модуль
        await utils.send_question(state, callback_query.message.chat.id, bot_id, bot)

    @router.callback_query(AnswerButton.filter())
    async def process_answer_callback(callback_query: CallbackQuery,
                                      callback_data: AnswerButton,
                                      state: FSMContext) -> None:
        # Удалим сообщение после ответа пользователя
        await callback_query.message.delete()
        # Получим состояние пользователя
        user_status = await state.get_state()
        # Если пользователь еще не заполнил анкету
        if user_status != Questionnaire.completed:
            data = await state.get_data()
            # Получим ответы пользователя из стейта
            answers = data['answers']
            # Получим id модуля (вопроса)
            question_id = data['question_id']
            # Добавим id вопроса в стейт в качестве предыдущего вопроса
            data['prev_questions'].append(question_id)
            # Запишем ответ в стейт
            answers[question_id] = callback_data.answer
            await state.update_data(answers=answers, prev_questions=data['prev_questions'])

            # Если есть следующий модуль
            if callback_data.next_id is not None and \
                    callback_data.next_id != 0 and \
                    (user_status != Questionnaire.on_approval or
                     str(callback_data.next_id) not in data['on_approval'].keys()):
                button_id = int(callback_data.next_id)
                await bot.send_chat_action(callback_query.message.chat.id, 'typing')
                # Отправим следующий модуль по id, на который указывает кнопка
                await state.update_data(question_id=button_id)
                await utils.send_question(state, callback_query.message.chat.id, bot_id, bot)
                await callback_query.answer(None)
            elif user_status == Questionnaire.on_approval:
                await utils.finish_questionnaire(state, callback_query.message.chat.id, bot_id,
                                                 bot, callback_data.next_id)
            # Если пользователь ответил на все вопросы
            else:
                await utils.finish_questionnaire(state, callback_query.message.chat.id, bot_id, bot)

        # Если пользователь уже заполнил анкету
        else:
            await bot.send_message(callback_query.message.chat.id, 'Вы уже прошли регистрацию!')

    await dp.start_polling(bot)


async def test():
    from dotenv import load_dotenv
    load_dotenv()
    tasks = [
        run_instance(66),
        run_instance(67)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(test())
