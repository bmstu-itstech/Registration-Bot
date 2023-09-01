import logging
import asyncio
import json
import asyncpg

from aiogram.fsm.context import FSMContext
from aiogram.client.bot import Bot

from .connector import connect_or_create
from ..custom_types import Questionnaire


async def write_data_from_file(filename: str, bot_id: int) -> None:
    """
    Функция для создания БД для нового бота из JSON.
    """

    f = open(filename)
    data = json.load(f)
    modules = data['journal']['modules']
    f.close()

    # Подключимся к БД
    conn = await connect_or_create('postgres', f'id{bot_id}')
    # Удалим все существующие таблицы для возможности перезаписи данных бота
    await conn.execute('''DROP TABLE IF EXISTS modules, buttons, answers''')

    # Создадим таблицу с вопросами
    await conn.execute('''
                CREATE TABLE modules (
                    id INTEGER PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer_type TEXT NOT NULL,
                    next_id INTEGER
                );
            ''')

    # Создадим таблицу с кнопками
    await conn.execute('''
                CREATE TABLE buttons (
                    current_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    next_id INTEGER
                );
            ''')
    
    # Создадим таблицу с ответами
    await conn.execute('''
                CREATE TABLE answers (
                    chat_id INTEGER PRIMARY KEY
                );
            ''')

    for module_id, module in modules.items():
        await conn.execute(
            '''
                INSERT INTO modules (id, question, answer_type, next_id)
                VALUES ($1, $2, $3, $4)
            ''',
            int(module_id), module['question'], module['answer_type'], module['next_id']
        )
        await conn.execute(f'''
                ALTER TABLE answers
                ADD COLUMN answer{module_id} TEXT;
            ''')
        buttons = module['buttons']
        for button in buttons:
            await conn.execute(
                '''
                    INSERT INTO buttons (current_id, answer, next_id)
                    VALUES ($1, $2, $3)
                ''',
                int(module_id), button['answer'], button['next_id']
            )


async def push_answers(state: FSMContext, chat_id: int, bot_id: int | str, bot: Bot) -> None:
    """
    Функция для отправки ответов пользователя в таблицу соответствующего бота.
    """

    # Установим соединение с БД
    conn = await connect_or_create('postgres', f'id{bot_id}')

    # Проверим, существует ли уже пользователь
    try:
        await conn.execute(f'INSERT INTO answers (chat_id) '
                            f'VALUES ({chat_id});')
    except asyncpg.exceptions.UniqueViolationError:
        logging.warning(f'User {chat_id} already exists. Rewriting answers.')

    # Запишем ответы в базу дынных
    answers = (await state.get_data())['answers']
    for answer_id in answers.keys():
        await conn.execute(f'UPDATE answers SET answer{answer_id} = $1 '
                            f'WHERE chat_id = $2;',
                            answers[answer_id], chat_id)

    # Поставим "завершенное" состояние анкете
    await state.set_state(Questionnaire.completed)
    await conn.close()
    await bot.send_message(chat_id, 'Ответы записаны!')


if __name__ == '__main__':
    asyncio.run(write_data_from_file('test.json', 1))
