import logging
import asyncio
import os

import emoji

import asyncpg.exceptions
from aiogram import Bot, Dispatcher, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Text, Command
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis

import connector

# Настроим логирование
logging.basicConfig(level=logging.INFO)


# Класс состояний
class Questionnaire(StatesGroup):
    # Показывает, что опрос в процессе прохождения
    in_process = State()
    # Показывает что опрос на стадии одобрения пользователем
    on_approval = State()
    # Показывает что опрос пройден
    completed = State()


class AnswerButtonCallback(CallbackData, prefix="answer_button", sep="#"):
    next_id: int | None
    answer: str


class QuestionButtonCallback(CallbackData, prefix="question_button"):
    question_id: int


# Set up startup handler
async def run_instance(token, bot_id):
    # Set up states
    logging.info(f'Starting bot id{bot_id}...')

    # Connect to redis
    redis = aioredis.Redis.from_url(f'redis://localhost:6379/{bot_id}')
    storage = RedisStorage(redis)

    questionnaire = Questionnaire()

    # Add Router
    router = Router()

    # Initialize telegram_bot and dispatcher
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    async def get_question(question_id: int):
        conn = await connector.connect_or_create('postgres', f'id{bot_id}')
        # Get module text from database
        module = await conn.fetchrow('SELECT * FROM modules WHERE id = $1',
                                     question_id)
        rows = await conn.fetch('SELECT (answer, next_id) FROM buttons '
                                'WHERE current_id = $1',
                                question_id)
        buttons = [row[0] for row in rows]
        await conn.close()
        return module, buttons

    async def send_question(state, chat_id: int) -> None:
        # Сейчас за id текущего вопроса полностью отвечает стейт, в теории можно его
        # передавать в аргументы функции send_question

        # Create database connection
        conn = await connector.connect_or_create('postgres', f'id{bot_id}')
        # Получим данные стейта
        data = await state.get_data()
        # Get module text and type from database
        module, buttons = await get_question(data['question_id'])
        question = module['question']
        keyboard = InlineKeyboardBuilder()

        if len(buttons) > 0:
            # Get module buttons from database (if applicable)
            for element in buttons:
                keyboard.button(callback_data=AnswerButtonCallback(answer=str(element[0]),
                                                                   next_id=element[1]).pack(),
                                text=str(element[0]))

        # Если уже был пройден хотя бы один вопрос, добавим кнопку "Назад"
        if len(data['prev_questions']) > 0 and await state.get_state() != questionnaire.on_approval:
            keyboard.button(callback_data='get_back', text=emoji.emojize(":reverse_button: Назад"))

        keyboard.adjust(1)
        message = await bot.send_message(chat_id, question, reply_markup=keyboard.as_markup())
        await state.update_data(question_id=data['question_id'], prev_message_id=message.message_id)
        await conn.close()

    async def push_answers(state, chat_id: int) -> None:
        # Create database connection
        conn = await connector.connect_or_create('postgres', f'id{bot_id}')
        # Check if user already exists
        try:
            await conn.execute(f'INSERT INTO answers (chat_id) '
                               f'VALUES ({chat_id});')
        except asyncpg.exceptions.UniqueViolationError:
            logging.warning(f'User {chat_id} already exists. Rewriting answers.')

        # Write answers to DB
        answers = (await state.get_data())['answers']
        for answer_id in answers.keys():
            await conn.execute(f'UPDATE answers SET answer{answer_id} = $1 '
                               f'WHERE chat_id = $2;',
                               answers[answer_id], chat_id)

        # Set state to "completed"
        await state.set_state(questionnaire.completed)
        await conn.close()
        await bot.send_message(chat_id, 'Ответы записаны!')

    async def finish_questionnaire(state, chat_id, next_question_id: int | None = None) -> None:
        user_status = await state.get_state()

        if user_status == questionnaire.on_approval:
            # Get state data
            data = await state.get_data()
            # Get temp and new answers
            temp_answers = data['on_approval']
            new_answers = data['answers']
            answers = dict()

            for temp_id in temp_answers.keys():
                if temp_id == list(new_answers.keys())[0]:
                    break
                answers[temp_id] = temp_answers[temp_id]

            for answer_id in new_answers.keys():
                answers[answer_id] = new_answers[answer_id]

            if next_question_id is not None:
                for temp_id in temp_answers.keys():
                    if int(temp_id) >= next_question_id:
                        answers[temp_id] = temp_answers[temp_id]

            await state.update_data(answers=answers, on_approval=None)

        await state.set_state(questionnaire.on_approval)
        conn = await connector.connect_or_create('postgres', f'id{bot_id}')

        # Build a keyboard
        keyboard = InlineKeyboardBuilder()
        keyboard.button(callback_data='questionnaire_over',
                        text=emoji.emojize('Отправить :check_mark_button:'))

        data = await state.get_data()
        # Get answers dict from the state data
        new_answers = data['answers']
        message = 'Ваши ответы:\n\n'

        for answer_id in new_answers.keys():
            message += emoji.emojize(':small_blue_diamond:')
            # TODO: По сути здесь можно запросить сокращенное название для отображения на кнопке
            question, _ = await get_question(int(answer_id))
            question_text = question['question']
            answer_text = new_answers[answer_id]
            message += f' {question_text}: {answer_text}\n'
            keyboard.button(callback_data=QuestionButtonCallback(question_id=answer_id).pack(),
                            text=question_text)
        message += '\nЕсли вы хотите что-то исправить - нажмите кнопку с нужным вопросом.\n' \
                   'Если всё в порядке - нажмите кнопку "Отправить".'
        keyboard.adjust(1)
        await bot.send_message(chat_id, message, reply_markup=keyboard.as_markup())
        await conn.close()

    # Start command
    @router.message(CommandStart())
    async def cmd_start(message: Message, state: FSMContext) -> None:
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != questionnaire.completed and \
                user_status != questionnaire.in_process and \
                user_status != questionnaire.on_approval:
            await state.set_state(questionnaire.in_process)
            await state.update_data(answers=dict(), prev_questions=list(), question_id=1)
            await send_question(state, message.chat.id)
        else:
            await message.answer('Вы уже заполнили анкету!')

    # Reset command
    @router.message(Command('reset_my_questionnaire_please'))
    async def cmd_reset(message: Message, state: FSMContext) -> None:
        await state.set_state(questionnaire.in_process)
        await state.update_data(answers=dict(), prev_questions=list(), question_id=1)
        await send_question(state, message.chat.id)

    @router.message()
    async def process_text(message: Message, state: FSMContext) -> None:
        await message.delete()
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != questionnaire.completed:
            data = await state.get_data()
            # Удалим предыдущее сообщение бота
            await bot.delete_message(message.chat.id, data['prev_message_id'])
            # Get next module id
            question_id = data['question_id']
            question, buttons = await get_question(question_id)
            if len(buttons) > 0:
                await message.answer('Чтобы ответить, нажмите на одну из кнопок')
                return
            next_id = question['next_id']
            # Добавим ответ в стейт
            answers = data['answers']
            answers[question_id] = message.text
            # Добавим id вопроса в стейт в качестве предыдущего вопроса
            data['prev_questions'].append(question_id)
            # Загрузим изменения в стейт
            await state.update_data(answers=answers, question_id=next_id, prev_questions=data['prev_questions'])

            if next_id is not None and \
                    (user_status != questionnaire.on_approval or
                     str(next_id) not in data['on_approval'].keys()):
                # Showing that telegram_bot is typing its module
                await bot.send_chat_action(message.chat.id, 'typing')
                # Send next module
                await send_question(state, message.chat.id)
            elif user_status == questionnaire.on_approval:
                await finish_questionnaire(state, message.chat.id, next_id)
            else:
                await finish_questionnaire(state, message.chat.id)
        # If the user has already passed the questionnaire
        else:
            await message.answer('Вы уже заполнили анкету!')

    # Questionnaire end handler
    @router.callback_query(Text('questionnaire_over'))
    async def process_questionnaire_over(callback_query: CallbackQuery,
                                         state: FSMContext) -> None:
        await callback_query.message.edit_reply_markup()
        await callback_query.answer('Ответы записаны!')
        await push_answers(state, callback_query.message.chat.id)

    @router.callback_query(Text('get_back'))
    async def process_get_back(callback_query: CallbackQuery,
                               state: FSMContext) -> None:
        # Удалим сообщение сразу после нажатия пользователя на кнопку
        await callback_query.message.delete()
        data = await state.get_data()
        previous_id = data['prev_questions'].pop()
        data['answers'].pop(data['question_id'], None)
        await state.update_data(prev_questions=data['prev_questions'], answers=data['answers'], question_id=previous_id)
        await send_question(state, callback_query.message.chat.id)

    # Question buttons handler, used at the end of the questionnaire
    @router.callback_query(QuestionButtonCallback.filter())
    async def process_question_callback(callback_query: CallbackQuery,
                                        callback_data: QuestionButtonCallback,
                                        state: FSMContext) -> None:
        await callback_query.message.delete()
        data = await state.get_data()
        answers = data['answers']
        # Write answers to temporary storage and reset main storage
        await state.update_data(on_approval=answers, answers=dict(), question_id=callback_data.question_id)
        # Send requested module
        await send_question(state, callback_query.message.chat.id)

    # Answer buttons handler
    @router.callback_query(AnswerButtonCallback.filter())
    async def process_answer_callback(callback_query: CallbackQuery,
                                      callback_data: AnswerButtonCallback,
                                      state: FSMContext) -> None:
        # Удалим сообщение после ответа пользователя
        await callback_query.message.delete()
        # Getting user state
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != questionnaire.completed:
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
                    (user_status != questionnaire.on_approval or
                     str(callback_data.next_id) not in data['on_approval'].keys()):
                button_id = int(callback_data.next_id)
                # Showing that telegram_bot is typing its module
                await bot.send_chat_action(callback_query.message.chat.id, 'typing')
                # Send next module based on button ID
                await state.update_data(question_id=button_id)
                await send_question(state, callback_query.message.chat.id)
                await callback_query.answer(None)
            elif user_status == questionnaire.on_approval:
                await finish_questionnaire(state, callback_query.message.chat.id, callback_data.next_id)
            # If the user passed all the questions
            else:
                await finish_questionnaire(state, callback_query.message.chat.id)

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
