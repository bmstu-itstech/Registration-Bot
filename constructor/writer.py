from constructor.tree import Tree
import asyncpg

# Эта функция будет заполнять данными дерево и связываться с микросервисом БД
async def create_tree(data, bot_id):
    tree_ent = Tree(bot_id)

    for key in data.keys():
        tree_ent.add_module(key, data[key]["links"], data[key]["question"], data[key]["answers"])

    # Написал максимально простой тест дерева на асинхронном SQLite
    async with asyncpg.connect(f'./id{bot_id}.db') as conn:

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

        await conn.execute("COMMIT;")
