import asyncpg
import asyncio

# Database connect function
async def connect_or_create(user, database) -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(user=user, database=database)
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user='postgres'
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{user}"',
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(user=user, database=database)

    return conn

# Эта функция будет заполнять данными дерево и связываться с микросервисом БД
async def create_tree(bot_id):
    # Create database connection
    conn = await connect_or_create('postgres', f'id{bot_id}')

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
                ('Как тебя зовут?', 'text', 3),
                ('Ты совершеннолетний?', 'buttons', NULL),
                ('Выбери свою любимую игру', 'buttons', NULL),
                ('Какой твой любимый цвет?', 'text', NULL);
        ''')

    await conn.execute('''
            INSERT INTO buttons (question_id, answer_text, next_question_id)
            VALUES
                (1, 'Начать', 2),
                (3, 'Да', 4),
                (3, 'Нет', 5),
                (4, 'GTA', NULL),
                (4, 'CSGO', NULL);
        ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id SERIAL PRIMARY KEY,
                user_id INT
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