import logging
import asyncio

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

from connection_router import connection

# Set up logging
logging.basicConfig(level=logging.INFO)


# State class
class Questionnaire(StatesGroup):
    # Stores current question id
    question_id = State()
    # Stores user's answers
    answers = State()
    # Shows that the questionnaire is in process
    in_process = State()
    # Shows that the questionnaire is completed
    completed = State()
    # Stores previous questions' ids
    previous = State()


class ButtonCallback(CallbackData, prefix="button"):
    question_id: int
    next_question_id: int | None
    answer_text: str


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

    async def get_question(conn, question_id):
        # Get question text from database
        question = await conn.fetchrow('SELECT * FROM questions WHERE id = $1',
                                       question_id)
        rows = await conn.fetch('SELECT (question_id, next_question_id, answer_text) FROM buttons '
                                'WHERE question_id = $1',
                                question_id)
        buttons = [row[0] for row in rows]
        return question, buttons

    async def get_next_question_id(question_id):
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')
        next_question_id = await conn.fetchrow('SELECT next_question_id FROM questions '
                                               'WHERE id = $1',
                                               question_id)
        return next_question_id[0]

    async def send_question(state, chat_id, question_id) -> None:
        # Create database connection
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')
        # Get question text and type from database
        question, buttons = await get_question(conn, question_id)
        question_text = question[0]
        question_type = question[1]

        # Send question
        if question_type == 'text':
            await bot.send_message(chat_id, question_text)
        elif question_type == 'buttons':
            # Get question options from database (if applicable)
            question_options = question[2]
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

    async def push_answers(state, user_id):
        # Create database connection
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')
        await conn.execute(f'INSERT INTO answers (user_id) '
                           f'VALUES ({user_id});')
        answers = (await state.get_data())['answers']
        for answer in answers:
            if answer[0] != 1:
                await conn.execute(f"UPDATE answers SET answer{answer[0]} = $1 "
                                   f"WHERE user_id = $2;",
                                   answer[1], user_id)
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
                # Showing that bot is typing its question
                await bot.send_chat_action(message.chat.id, 'typing')
                # Send next question
                await send_question(state, message.chat.id, next_question_id)
            else:
                await push_answers(state, message.chat.id)
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
        # Deleting message with buttons after the answer
        await callback_query.message.delete()
        # Alternative:
        # await callback_query.message.edit_reply_markup()
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
            if callback_data.next_question_id is not None:
                button_id = int(callback_data.next_question_id)
                # Showing that bot is typing its question
                await bot.send_chat_action(callback_query.message.chat.id, 'typing')
                # Send next question based on button ID
                await send_question(state, callback_query.message.chat.id, button_id)
                await callback_query.answer(None)

            # If the user passed all the questions
            else:
                await push_answers(state, callback_query.message.chat.id)
                await callback_query.answer('Ответы записаны!')
                await bot.send_message(callback_query.message.chat.id, 'Ответы записаны!')
        # If the user has already passed the questionnaire
        else:
            await bot.send_message(callback_query.message.chat.id,
                                   'Вы уже проходили тест! Для повторного прохождения напишите /start')

    await dp.start_polling(bot)


async def main():
    import config
    tasks = [
        run_instance(config.bot_token, 1),
        run_instance(config.bot_token2, 2)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
