"""
Дерево из модулей. Так как можно каждый раз получать из API дерево модулей заново,
необходимости в хранении списка предыдущих модулей нет - метод удаления одного модуля не нужен,
так как структура при изменении каждый раз будет перезаписываться по новой.

P.S. Стоит вопрос о том, нужна ли вообще структура дерева, если мы все равно
все данные сразу запишем в БД и сможем их в любое время получить
"""

from constructor.module import Module


class Tree:

    def __init__(self, bot_id):
        self._bot_id = bot_id
        self.modules = {}

    def add_module(self, module_id, next_ids, question_text, answers):
        self.modules[module_id] = Module(next_ids, question_text, answers)

    def get_data(self):
        data = []

        for key in self.modules.keys():
            if self.modules[key].get_answers() is not None:
                answers = "/".join(str(x) for x in self.modules[key].get_answers())
            else:
                answers = None

            if len(self.modules[key].get_next_ids()) > 0:
                ids = "/".join(str(x) for x in self.modules[key].get_next_ids())
            else:
                ids = None

            data.append((key, ids, self.modules[key].get_question(), answers))

        return data
