import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis

# Set up logging
logging.basicConfig(level=logging.INFO)


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
    question_text = await conn.fetch('SELECT question_text FROM questions WHERE id = $1',
                                     question_id)
    return question_text[0]


async def get_question_type(conn, question_id):
    # Get question type from database
    question_type = await conn.fetch('SELECT question_type FROM questions WHERE id = $1',
                                     question_id)
    return question_type[0]


async def get_question_options(conn, question_id):
    # Get question options from database
    question_options = await conn.fetch('SELECT (id, answer_text) FROM buttons WHERE question_id = $1',
                                        question_id)
    return question_options[0] if question_options is not None else None


async def get_next_question_id(conn, button_id):
    # Get next question ID based on button ID
    next_question_id = await conn.fetch('SELECT next_question_id FROM buttons WHERE id = $1',
                                        button_id)
    return next_question_id[0]


async def send_question(bot_id, state, bot, chat_id, question_id):
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

        keyboard = InlineKeyboardMarkup(row_width=1)

        for option in question_options:
            button = InlineKeyboardButton(text=option[1], callback_data=option[0])
            keyboard.construct(button)

        await bot.send_message(chat_id, question_text, reply_markup=keyboard)

    await state.update_data(question_id=question_id)


# Set up startup handler
async def run_instance(token, bot_id):
    # Set up states
    class Questionnaire(StatesGroup):
        question_id = State()

    logging.info('Starting bot...')

    redis = aioredis.Redis.from_url(f'redis://localhost:6379/{bot_id}')
    storage = RedisStorage(redis)

    # Add Router
    router = Router()

    # Initialize bot and dispatcher
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    # Create database connection
    conn = await connect_or_create('postgres', f'id{bot_id}')

    # Create questions table
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL
            );
        ''')

    # Create buttons table
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS buttons (
                id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL,
                answer_text TEXT NOT NULL,
                next_question_id INTEGER,
                FOREIGN KEY (question_id) REFERENCES questions(id)
            );
        ''')

    # Insert sample data
    await conn.execute('''
            INSERT INTO questions (question_text, question_type)
            VALUES
                ('Как тебя зовут?', 'text'),
                ('Ты совершеннолетний?', 'text'),
                ('Какой твой любимый цвет?', 'buttons'),
                ('То есть ты фанат красного?', 'buttons'),
                ('То есть ты фанат синего?', 'buttons');
        ''')

    await conn.execute('''
            INSERT INTO buttons (question_id, answer_text, next_question_id)
            VALUES
                (3, 'Красный', 4),
                (3, 'Синий', 5),
                (4, 'Да', NULL),
                (4, 'Нет', NULL),
                (5, 'Да', NULL),
                (5, 'Нет', NULL);
        ''')

    await conn.close()

    @router.message()
    async def answer_handler(message: types.Message, state: FSMContext):
        # Get current question ID from state
        data = await state.get_data()
        question_id = data.get('question_id', 1)
        next_question_id = question_id + 1

        # Send next question
        await send_question(bot_id, state, bot, message.chat.id, next_question_id)

    # Start command
    @router.message(CommandStart())
    async def cmd_start(message: types.Message, state: FSMContext):
        await send_question(bot_id, state, bot, message.chat.id, 1)

    # Callback query handler
    @router.callback_query()
    async def process_callback(callback_query: CallbackQuery, state: FSMContext):
        # Get button ID from callback data
        button_id = callback_query.data

        # Send next question based on button ID
        await send_question(bot_id, state, bot, callback_query.message.chat.id, button_id)

    await dp.start_polling(bot)


if __name__ == '__main__':
    import config

    asyncio.run(run_instance(config.bot_token, 1))
