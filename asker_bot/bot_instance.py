import asyncio
import logging
import asyncpg
import magic_filter

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis

# Set up logging
logging.basicConfig(level=logging.INFO)


# State class
class Questionnaire(StatesGroup):
    # Будет хранить id текущего вопроса
    question_id = State()
    # Будет хранить ответы пользователя
    answers = State()
    # Будет обозначать прохождение анкеты
    in_process = State()
    # Будет обозначать завершенное состояние анкетирования
    completed = State()


class ButtonCallback(CallbackData, prefix="button"):
    question_id: int
    next_question_id: str
    answer_text: str


# Database connect function
async def connect_or_create(user, database) -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(user=user, database=database)
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it
        sys_conn = await asyncpg.connect(
            database='template1',
            user='postgres'
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{user}"',
        )
        await sys_conn.close()

        # Connect to the newly created database
        conn = await asyncpg.connect(user=user, database=database)

    return conn


# Set up startup handler
async def run_instance(token, bot_id):
    # Set up states
    logging.info(f'Starting bot id{bot_id}...')

    # Connect to redis
    redis = aioredis.Redis.from_url(f'redis://localhost:6380/{bot_id}')
    storage = RedisStorage(redis)

    questionnaire = Questionnaire()

    # Add Router
    router = Router()

    # Initialize bot and dispatcher
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    async def get_question_text(conn, question_id):
        # Get question text from database
        question_text = await conn.fetchrow('SELECT question_text FROM questions WHERE id = $1',
                                            question_id)
        return question_text[0]

    async def get_question_type(conn, question_id):
        # Get question type from database
        question_type = await conn.fetchrow('SELECT question_type FROM questions WHERE id = $1',
                                            question_id)
        return question_type[0]

    async def get_question_options(conn, question_id):
        # Get question options from database
        rows = await conn.fetch('SELECT (question_id, next_question_id, answer_text) FROM buttons '
                                'WHERE question_id = $1',
                                question_id)
        question_options = [row[0] for row in rows]
        return question_options

    async def send_question(state, chat_id, question_id) -> None:
        # Create database connection
        conn = await connect_or_create('postgres', f'id{bot_id}')
        # Get question text and type from database
        question_text = await get_question_text(conn, question_id)
        question_type = await get_question_type(conn, question_id)

        # Send question
        if question_type == 'text':
            await bot.send_message(chat_id, question_text)
        elif question_type == 'buttons':
            # Get question options from database (if applicable)
            question_options = await get_question_options(conn, question_id)
            keyboard = InlineKeyboardBuilder()

            for element in question_options:
                # Symbol ; is used to split callback_data
                keyboard.button(callback_data=ButtonCallback(question_id=element[0],
                                                             next_question_id=str(element[1]),
                                                             answer_text=element[2]).pack(),
                                text=str(element[2]))

            await bot.send_message(chat_id, question_text, reply_markup=keyboard.as_markup())

        await state.update_data(question_id=question_id)
        await conn.close()

    async def get_next_question_id(question_id):
        conn = await connect_or_create('postgres', f'id{bot_id}')
        next_question_id = await conn.fetchrow('SELECT next_question_id FROM questions '
                                               'WHERE id = $1',
                                               question_id)
        return next_question_id[0]

    async def finish_questionnaire(state, user_id):
        # Create database connection
        conn = await connect_or_create('postgres', f'id{bot_id}')
        await conn.execute(f'INSERT INTO answers (user_id) '
                           f'VALUES ({user_id});')
        answers = (await state.get_data())['answers']
        for answer in answers:
            if answer[0] != 1:
                await conn.execute(f"UPDATE answers SET answer{answer[0]} = '{answer[1]}' "
                                   f"WHERE user_id = {user_id};")
        await state.set_state(questionnaire.completed)
        await conn.close()

    # Start command
    @router.message(CommandStart())
    async def cmd_start(message: types.Message, state: FSMContext) -> None:
        await state.set_state(questionnaire.in_process)
        await state.update_data(answers=[])
        await send_question(state, message.chat.id, 1)

    @router.message()
    async def process_text(message: types.Message, state: FSMContext) -> None:
        user_status = await state.get_state()
        if user_status == questionnaire.in_process:
            data = await state.get_data()
            # Get answers list from the state
            answers = data['answers']
            # Get the question id
            question_id = data['question_id']
            # Write the answer to the state
            answers.append((question_id, message.text))
            await state.update_data(answers=answers)
            # Get next question id
            next_question_id = await get_next_question_id(question_id)

            if next_question_id is not None:
                # Send next question
                await send_question(state, message.chat.id, next_question_id)
            else:
                await finish_questionnaire(state, message.from_user.id)
                await message.answer('Ответы записаны!')
        # If the user has already passed the questionnaire
        else:
            await message.answer('Вы уже проходили тест! Для повторного прохождения '
                                 'напишите /start')

    # Callback query handler
    @router.callback_query(ButtonCallback.filter())
    async def process_callback(callback_query: CallbackQuery,
                               callback_data: ButtonCallback,
                               state: FSMContext) -> None:
        user_status = await state.get_state()
        if user_status == questionnaire.in_process:
            data = await state.get_data()
            # Get answers list from the state
            answers = data['answers']
            # Get the question id
            question_id = data['question_id']
            # Write the answer to the state
            answers.append((question_id, callback_data.answer_text))
            await state.update_data(answers=answers)

            # If there is next question
            if callback_data.next_question_id != 'None':
                button_id = int(callback_data.next_question_id)
                # Send next question based on button ID
                await send_question(state, callback_query.message.chat.id, button_id)
                await callback_query.answer(None)

            # If the user passed all the questions
            else:
                await finish_questionnaire(state, callback_query.from_user.id)
                await callback_query.answer('Ответы записаны!')
                await bot.send_message(callback_query.message.chat.id, 'Ответы записаны!')
        # If the user has already passed the questionnaire
        else:
            await bot.send_message(callback_query.message.chat.id,
                                   'Вы уже проходили тест! Для повторного прохождения напишите /start')

    await dp.start_polling(bot)


if __name__ == '__main__':
    import config

    asyncio.run(run_instance(config.bot_token, 1))
