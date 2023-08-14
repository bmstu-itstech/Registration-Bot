import asyncio
import json

from bot import connection


# Функция для создания БД из JSON для нового бота
async def write_data_from_file(filename: str, bot_id: int) -> None:
    f = open(filename)
    data = json.load(f)
    modules = data['journal']['modules']
    f.close()

    # Подключимся к БД
    conn = await connection.connect_or_create('postgres', f'id{bot_id}')
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


if __name__ == '__main__':
    asyncio.run(write_data_from_file('test.json', 1))
