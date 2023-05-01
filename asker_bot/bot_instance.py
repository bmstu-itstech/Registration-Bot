import logging
import asyncio
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
    # Shows that the questionnaire is on user's approve
    on_approval = State()
    # Shows that the questionnaire is completed
    completed = State()


class AnswerButtonCallback(CallbackData, prefix="answer_button"):
    question_id: int
    next_question_id: int | None
    answer_text: str


class QuestionButtonCallback(CallbackData, prefix="question_button"):
    question_id: int


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

    async def get_question(question_id: int):
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')
        # Get question text from database
        question = await conn.fetchrow('SELECT * FROM questions WHERE id = $1',
                                       question_id)
        rows = await conn.fetch('SELECT (question_id, next_question_id, answer_text) FROM buttons '
                                'WHERE question_id = $1',
                                question_id)
        buttons = [row[0] for row in rows]
        await conn.close()
        return question, buttons

    async def send_question(state, chat_id: int, question_id: int) -> None:
        # Create database connection
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')
        # Get question text and type from database
        question, buttons = await get_question(question_id)
        question_text = question['question_text']
        question_type = question['question_type']

        # Send question
        if question_type == 'text':
            await bot.send_message(chat_id, question_text)
        elif question_type == 'buttons':
            # Get question buttons from database (if applicable)
            keyboard = InlineKeyboardBuilder()
            for element in buttons:
                keyboard.button(callback_data=AnswerButtonCallback(question_id=element[0],
                                                                   next_question_id=str(element[1]),
                                                                   answer_text=element[2]).pack(),
                                text=str(element[2]))
            await bot.send_message(chat_id, question_text, reply_markup=keyboard.as_markup())

        await state.update_data(question_id=question_id)
        await conn.close()

    async def push_answers(state, chat_id: int) -> None:
        # Create database connection
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')
        # Check if user already exists
        try:
            await conn.execute(f'INSERT INTO answers (chat_id) '
                               f'VALUES ({chat_id});')
        except asyncpg.exceptions.UniqueViolationError as e:
            logging.warning(f'User {chat_id} already exists. Rewriting answers.')

        # Write answers to DB
        answers = (await state.get_data())['answers']
        for answer_id in answers.keys():
            if answer_id != '1':
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
        conn = await connection.connect_or_create('postgres', f'id{bot_id}')

        # Build a keyboard
        keyboard = InlineKeyboardBuilder()
        keyboard.button(callback_data='questionnaire_over',
                        text=f'Отправить {emoji.emojize(":check_mark_button:")}')

        data = await state.get_data()
        # Get answers dict from the state data
        new_answers = data['answers']
        message = 'Ваши ответы:\n\n'

        for answer_id in new_answers.keys():
            if answer_id != '1':
                message += emoji.emojize(':small_blue_diamond:')
                question, _ = await get_question(int(answer_id))
                question_text = question['question_text']
                answer_text = new_answers[answer_id]
                message += f' {question_text}: {answer_text}\n'
                keyboard.button(callback_data=QuestionButtonCallback(question_id=answer_id).pack(),
                                text=question_text)
        message += '\nЕсли вы хотите что-то исправить - нажмите кнопку с нужным вопросом.\n' \
                   'Если всё в порядке - нажмите кнопку "Отправить".'
        keyboard.adjust(1, repeat=True)
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
            await state.update_data(answers=dict())
            await send_question(state, message.chat.id, 1)
        else:
            await message.answer('Вы уже заполнили анкету!')

    # Reset command
    @router.message(Command('reset_my_questionnaire_please'))
    async def cmd_reset(message: Message, state: FSMContext) -> None:
        await state.set_state(questionnaire.in_process)
        await state.update_data(answers=dict())
        await send_question(state, message.chat.id, 1)

    @router.message()
    async def process_text(message: Message, state: FSMContext) -> None:
        user_status = await state.get_state()
        # If the user hasn't already passed the questionnaire
        if user_status != questionnaire.completed:
            data = await state.get_data()
            # Get answers dict from the state
            answers = data['answers']
            # Get the question id
            question_id = data['question_id']
            # Write the answer to the state
            answers[question_id] = message.text
            await state.update_data(answers=answers)
            # Get next question id
            question, _ = await get_question(question_id)
            next_question_id = question['next_question_id']

            if next_question_id is not None and \
                    (user_status != questionnaire.on_approval or
                     str(next_question_id) not in data['on_approval'].keys()):
                # Showing that bot is typing its question
                await bot.send_chat_action(message.chat.id, 'typing')
                # Send next question
                await send_question(state, message.chat.id, next_question_id)
            elif user_status == questionnaire.on_approval:
                await finish_questionnaire(state, message.chat.id, next_question_id)
            else:
                await finish_questionnaire(state, message.chat.id)
        # If the user has already passed the questionnaire
        else:
            await message.answer('Вы уже заполнили анкету!')

    # Questionnaire end handler
    @router.callback_query(Text('questionnaire_over'))
    async def process_questionnaire_over(callback_query: CallbackQuery,
                                         state: FSMContext) -> None:
        await callback_query.message.delete()
        await callback_query.answer('Ответы записаны!')
        await push_answers(state, callback_query.message.chat.id)

    # Question buttons handler, used at the end of the questionnaire
    @router.callback_query(QuestionButtonCallback.filter())
    async def process_question_callback(callback_query: CallbackQuery,
                                        callback_data: QuestionButtonCallback,
                                        state: FSMContext) -> None:
        await callback_query.message.delete()
        data = await state.get_data()
        answers = data['answers']
        # Write answers to temporary storage and reset main storage
        await state.update_data(on_approval=answers, answers=dict())
        # Send requested question
        await send_question(state, callback_query.message.chat.id, callback_data.question_id)

    # Answer buttons handler
    @router.callback_query(AnswerButtonCallback.filter())
    async def process_answer_callback(callback_query: CallbackQuery,
                                      callback_data: AnswerButtonCallback,
                                      state: FSMContext) -> None:
        user_status = await state.get_state()
        # Deleting message with buttons after the answer
        await callback_query.message.delete()
        # If the user hasn't already passed the questionnaire
        if user_status != questionnaire.completed:
            data = await state.get_data()
            # Get answers dict from the state
            answers = data['answers']
            # Get the question id
            question_id = data['question_id']
            # Write the answer to the state
            answers[question_id] = callback_data.answer_text
            await state.update_data(answers=answers)

            # If there is next question
            if callback_data.next_question_id is not None and \
                    (user_status != questionnaire.on_approval or
                     str(callback_data.next_question_id) not in data['on_approval'].keys()):
                button_id = int(callback_data.next_question_id)
                # Showing that bot is typing its question
                await bot.send_chat_action(callback_query.message.chat.id, 'typing')
                # Send next question based on button ID
                await send_question(state, callback_query.message.chat.id, button_id)
                await callback_query.answer(None)
            elif user_status == questionnaire.on_approval:
                await finish_questionnaire(state, callback_query.message.chat.id, callback_data.next_question_id)
            # If the user passed all the questions
            else:
                await finish_questionnaire(state, callback_query.message.chat.id)

        # If the user has already passed the questionnaire
        else:
            await bot.send_message(callback_query.message.chat.id, 'Вы уже заполнили анкету!')

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
