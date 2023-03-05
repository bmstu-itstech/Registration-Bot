from constructor.tree import Tree
import sqlite3


# Эта функция будет заполнять данными дерево и связываться с микросервисом БД
def create_tree(data, bot_id):
    tree_ent = Tree(bot_id)

    for module in data:
        tree_ent.add_module(module[0], module[1], module[2], module[3])

    # Написал максимально простой тест дерева на SQLite
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        sql = (
            f"DROP TABLE IF EXISTS id{bot_id}"
        )
        cursor.execute(sql)

        sql = (
            f"CREATE TABLE id{bot_id} ("
            f"module_id INTEGER PRIMARY KEY,"
            f"next_ids text,"
            f"question_text text NOT NULL,"
            f"answers text)"
        )
        cursor.execute(sql)

        for module in tree_ent.get_data():
            sql = (
                f"INSERT INTO id{bot_id} (module_id, next_ids, question_text, answers)"
                f"VALUES (?, ?, ?, ?)"
            )
            cursor.execute(sql, module)
        cursor.execute("COMMIT;")

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def read_tree(bot_id):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        module_id = 1
        prev_array = []
        while True:
            sql = (
                f'SELECT next_ids, question_text, answers '
                f'FROM id{bot_id} WHERE module_id={module_id}'
            )
            cursor.execute(sql)
            data = cursor.fetchall()[0]

            try:
                next_ids = data[0].split("/")
            except AttributeError:
                next_ids = None
            try:
                answers = data[2].split("/")
            except AttributeError:
                answers = None

            question_text = data[1]

            if len(prev_array) > 0:
                prev_id = prev_array[-1]
            else:
                prev_id = None

            print(f"Question: {question_text}, ID: {module_id}\n"
                  f"Previous question: {prev_id}")

            if answers is None:
                input_answer = input()
                if input_answer.lower().strip() == "back" and prev_id is not None:
                    module_id = prev_id
                    prev_array.pop(-1)
                elif input_answer.lower().strip() == "back":
                    print(f"No previous questions!")
                elif next_ids is not None:
                    prev_array.append(module_id)
                    module_id = next_ids[0]
                else:
                    break
            else:
                print(f"Answers: {answers}")
                input_answer = input()
                if input_answer.lower().strip() == "back" and prev_id is not None:
                    module_id = prev_id
                    prev_array.pop(-1)
                elif input_answer.lower().strip() == "back":
                    print(f"No previous questions!")
                else:
                    index = answers.index(input_answer.lower().strip())
                    prev_array.append(module_id)
                    module_id = next_ids[index]

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
