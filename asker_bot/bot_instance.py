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
    async with asyncpg.connect(f'id{bot_id}.db') as conn:

        # Create questions table
        await conn.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    question_text TEXT NOT NULL,
                    type TEXT NOT NULL DEFAULT "text"
                )
            ''')

        # Create buttons table
        await conn.execute('''
                CREATE TABLE IF NOT EXISTS buttons (
                    id INTEGER PRIMARY KEY,
                    question_id INTEGER NOT NULL,
                    answer_text TEXT NOT NULL,
                    next_question_id INTEGER,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            ''')

        # Insert sample data
        await conn.execute('''
                INSERT INTO questions (question_text, type)
                VALUES
                    ("Как тебя зовут?", "text"),
                    ("Ты совершеннолетний?", "text"),
                    ("Какой твой любимый цвет?", "buttons"),
                    ("То есть ты фанат красного?", "buttons"),
                    ("То есть ты фанат синего?", "buttons")
            ''')

        await conn.execute('''
                INSERT INTO buttons (question_id, answer_text, next_question_id)
                VALUES
                    (3, "Красный", 4),
                    (3, "Синий", 5),
                    (4, "Да", NULL),
                    (4, "Нет", NULL),
                    (5, "Да", NULL),
                    (5, "Нет", NULL)
            ''')

        await conn.commit()

    async def get_question_text(conn, question_id):
        # Get question text from database
        await conn.fetchrow('SELECT question_text FROM questions WHERE id = ?',
                           (question_id,))
        question_text = (await conn.fetchone())[0]
        return question_text

    async def get_question_type(conn, question_id):
        # Get question type from database
        question_type =await conn.fetchrow('SELECT type FROM questions WHERE id = ?',
                           (question_id,))
        return question_type[0]

    async def get_question_options(cursor, question_id):
        # Get question options from database
        await cursor.execute('SELECT (id, answer_text) FROM buttons WHERE question_id = ?',
                       (question_id,))
        question_options = (await cursor.fetchall())
        return question_options[0] if question_options is not None else None

    async def get_next_question_id(cursor, button_id):
        # Get next question ID based on button ID
        await cursor.execute('SELECT next_question_id FROM buttons WHERE id = ?',
                       (button_id,))
        next_question_id = (await cursor.fetchone())[0]
        return next_question_id

    async def send_question(state, bot, chat_id, question_id):
        async with asyncpg.connect(f'id{bot_id}.db') as db:
            cursor = await db.cursor()
            # Get question text and type from database
            question_text = await get_question_text(cursor, question_id)
            question_type = await get_question_type(cursor, question_id)

        # Send question
        if question_type == 'text':
            await bot.send_message(chat_id, question_text)
        elif question_type == 'buttons':
            # Get question options from database (if applicable)
            question_options = await get_question_options(cursor, question_id)

            keyboard = InlineKeyboardMarkup(row_width=1)

            for option in question_options:
                button = InlineKeyboardButton(text=option[1], callback_data=option[0])
                keyboard.construct(button)

            await bot.send_message(chat_id, question_text, reply_markup=keyboard)


        await state.update_data(question_id=question_id)

    @router.message()
    async def answer_handler(message: types.Message, state: FSMContext):
        # Get current question ID from state
        data = await state.get_data()
        question_id = data.get('question_id', 1)
        next_question_id = question_id + 1

        # Send next question
        await send_question(state, bot, message.chat.id, next_question_id)

    # Start command
    @router.message(CommandStart())
    async def cmd_start(message: types.Message, state: FSMContext):
        await send_question(state, bot, message.chat.id, 1)

    # Callback query handler
    @router.callback_query()
    async def process_callback(callback_query: CallbackQuery, state: FSMContext):
        # Get button ID from callback data
        button_id = callback_query.data

        # Send next question based on button ID
        await send_question(state, bot, callback_query.message.chat.id, button_id)

    # # Default message
    # @router.message()
    # async def default_handler(message: types.Message):
    #     await bot.send_message(message.chat.id, 'Неверный формат сообщения!')

    async def main():
        await dp.start_polling(bot)

    await main()