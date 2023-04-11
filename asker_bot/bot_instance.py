import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher, types, Router
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
    # Будет хранить id текущего вопроса и обозначать момент прохождения анкеты
    in_process = State()
    # Будет обозначать завершенное состояние анкетирования
    completed = State()


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
    rows = await conn.fetch('SELECT (next_question_id, answer_text) FROM buttons WHERE question_id = $1',
                                        question_id)
    question_options = [dict(row) for row in rows]
    return question_options


async def send_question(bot_id, bot, state, chat_id, question_id) -> None:
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
            keyboard.button(callback_data=str(element['row'][0]), text=str(element['row'][1]))

        await bot.send_message(chat_id, question_text, reply_markup=keyboard.as_markup())

    await state.update_data(question_id=question_id)


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

    # Initialize bot and dispatcher
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)


    # Start command
    @router.message(CommandStart())
    async def cmd_start(message: types.Message, state: FSMContext) -> None:
        await state.set_state(questionnaire.in_process)
        await state.update_data(in_process=1)
        await send_question(bot_id, bot, state, message.chat.id, 1)

    @router.message()
    async def process_text(message: types.Message, state: FSMContext) -> None:
        data = await state.get_data()
        question_id = data['in_process']
        next_question_id = question_id + 1

        # Send next question
        await send_question(bot_id, bot, state, message.chat.id, next_question_id)

    # Callback query handler
    @router.callback_query()
    async def process_callback(callback_query: CallbackQuery, state: FSMContext) -> None:
        user_id = callback_query.from_user.id
        # Get button ID from callback data
        if callback_query.data != 'None':
            button_id = int(callback_query.data)
            # Send next question based on button ID
            await send_question(bot_id, bot, state, callback_query.message.chat.id, button_id)

        # If the user passed all the questions
        else:
            await bot.send_message(callback_query.message.chat.id, 'Ответы записаны!')
            await state.set_state(questionnaire.completed)


    await dp.start_polling(bot)


if __name__ == '__main__':
    import config
    asyncio.run(run_instance(config.bot_token, 1))
