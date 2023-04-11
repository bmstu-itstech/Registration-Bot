from constructor.tree import Tree
import asyncpg

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
async def create_tree(data, bot_id):
    tree_ent = Tree(bot_id)

    for key in data.keys():
        tree_ent.add_module(key, data[key]["links"], data[key]["question"], data[key]["answers"])

    # Create database connection
    conn = await connect_or_create('postgres', f'id{bot_id}')

    sql = (
        f"DROP TABLE IF EXISTS id{bot_id}"
    )
    await conn.execute(sql)

    sql = (
        f"CREATE TABLE id{bot_id} ("
        f"module_id INTEGER PRIMARY KEY,"
        f"next_ids text,"
        f"question_text text NOT NULL,"
        f"answers text)"
    )
    await conn.execute(sql)

    for module in tree_ent.get_data():
        sql = (
            f"INSERT INTO id{bot_id} (module_id, next_ids, question_text, answers) "
            f"VALUES (?, ?, ?, ?)"
        )
        await conn.execute(sql, module)
