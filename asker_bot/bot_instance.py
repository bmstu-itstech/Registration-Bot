import asyncio
import logging
import aiosqlite

from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up startup handler
async def run_instance(token, bot_id):
    # Set up states
    class Questionnaire(StatesGroup):
        question_id = State()

    logging.info('Starting bot...')

    redis = Redis.from_url('redis://localhost:6379/1')
    storage = RedisStorage(redis)

    # Add Router
    router = Router()

    # Initialize bot and dispatcher
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    # Create database connection
    async with aiosqlite.connect(f'id{bot_id}.db') as db:
        cursor = await db.cursor()

        # Create questions table
        await cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    question_text TEXT NOT NULL,
                    answer TEXT,
                    has_buttons INTEGER NOT NULL DEFAULT 0
                )
            ''')

        # Create buttons table
        await cursor.execute('''
                CREATE TABLE IF NOT EXISTS buttons (
                    id INTEGER PRIMARY KEY,
                    question_id INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    next_question_id INTEGER,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            ''')

        # Insert sample data
        await cursor.execute('''
                INSERT INTO questions (question_text, answer, has_buttons)
                VALUES
                    ("Как тебя зовут?", NULL, 0),
                    ("Ты совершеннолетний?", NULL, 0),
                    ("Какой твой любимый цвет?", NULL, 1),
                    ("То есть ты фанат красного?", NULL, 1),
                    ("То есть ты фанат синего?", NULL, 1)
            ''')

        await cursor.execute('''
                INSERT INTO buttons (question_id, question_text, next_question_id)
                VALUES
                    (3, "Красный", 4),
                    (3, "Синий", 5),
                    (4, "Да", NULL),
                    (4, "Нет", NULL),
                    (5, "Да", NULL),
                    (5, "Нет", NULL)
            ''')

        await db.commit()

    async def get_question_text(cursor, question_id):
        # Get question text from database
        cursor.execute('SELECT question_text FROM questions WHERE id = ?',
                       (question_id,))
        question_text = cursor.fetchone()[0]
        return question_text

    async def get_question_type(cursor, question_id):
        # Get question type from database
        cursor.execute('SELECT type FROM questions WHERE id = ?',
                       (question_id,))
        question_type = cursor.fetchone()[0]
        return question_type

    async def get_question_options(cursor, question_id):
        # Get question options from database
        cursor.execute('SELECT options FROM questions WHERE id = ?',
                       (question_id,))
        question_options = cursor.fetchone()[0]
        return question_options.split(',') if question_options is not None else None

    async def get_next_question_id(cursor, button_id):
        # Get next question ID based on button ID
        cursor.execute('SELECT next_question_id FROM question_options WHERE button_id = ?',
                       (button_id,))
        next_question_id = cursor.fetchone()[0]
        return next_question_id

    async def send_question(state, bot, chat_id, question_id):
        async with aiosqlite.connect(f'id{bot_id}.db') as db:
            cursor = await db.cursor()
            # Get question text and type from database
            question_text = await get_question_text(cursor, question_id)
            question_type = await get_question_type(cursor, question_id)

            # Get question options from database (if applicable)
            question_options = await get_question_options(cursor, question_id)

        # Send question
        if question_type == 'text':
            await bot.send_message(chat_id, question_text)
        elif question_type == 'buttons':
            keyboard = InlineKeyboardMarkup(row_width=1)

            for option in question_options:
                button = InlineKeyboardButton(text=option, callback_data=option)
                keyboard.construct(button)

            await bot.send_message(chat_id, question_text, reply_markup=keyboard)

        await state.update_data(question_id=question_id)

    async def send_next_question(state, bot, chat_id, button_id=None):
        # Get current question ID from state
        async with state.get_data() as data:
            question_id = data.get('question_id')

        # Get next question ID from database
        if button_id is not None:
            async with aiosqlite.connect(f'id{bot_id}.db') as db:
                cursor = await db.cursor()
                next_question_id = await get_next_question_id(cursor, button_id)
        else:
            next_question_id = question_id + 1

        # Send next question
        await send_question(state, bot, chat_id, next_question_id)

    # Start command
    @router.message(CommandStart())
    async def cmd_start(message: types.Message, state: FSMContext):
        await send_next_question(state, bot, message.chat.id)

    # Callback query handler
    @router.callback_query(lambda c: True)
    async def process_callback(callback_query: CallbackQuery, state: FSMContext):
        # Get button ID from callback data
        button_id = callback_query.data

        # Send next question based on button ID
        await send_next_question(state, bot, callback_query.message.chat.id, button_id)

    # Default message
    @router.message()
    async def default_handler(message: types.Message):
        await bot.send_message(message.chat.id, 'Неверный формат сообщения!')

    async def main():
        await dp.start_polling(bot)

    await main()