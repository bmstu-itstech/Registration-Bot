import asyncio

from connection_router import connection


# The function will create tables for bot
async def create_tree(bot_id):
    # Create database connection
    conn = await connection.connect_or_create('postgres', f'id{bot_id}')

    # Create questions table
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL,
                next_question_id INTEGER
            );
        ''')

    # Create buttons table
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS buttons (
                id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL,
                answer_text TEXT NOT NULL,
                next_question_id INTEGER,
                FOREIGN KEY (question_id) REFERENCES questions(id),
                FOREIGN KEY (next_question_id) REFERENCES questions(id)
            );
        ''')

    # Insert sample data
    await conn.execute('''
            INSERT INTO questions (question_text, question_type, next_question_id)
            VALUES
                ('Привет! Я тестовый бот-опросник!', 'buttons', 2),
                ('Как тебя зовут? (ФИО)', 'text', 3),
                ('Ты из МГТУ?', 'buttons', NULL),
                ('Напиши номер своей группы', 'text', NULL),
                ('Из какого ты ВУЗа?', 'text', NULL);
        ''')

    await conn.execute('''
            INSERT INTO buttons (question_id, answer_text, next_question_id)
            VALUES
                (1, 'Начать', 2),
                (3, 'Да', 4),
                (3, 'Нет', 5);
        ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                chat_id INT PRIMARY KEY
            );
        ''')

    for i in range(2, 6):
        await conn.execute(f'''
                ALTER TABLE answers
                ADD COLUMN answer{i} TEXT;
            ''')

    await conn.close()


if __name__ == '__main__':
    asyncio.run(create_tree(1))
