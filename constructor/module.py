"""
Класс модуля. Простая структура с id следующих модулей
"""


class Module:

    def __init__(self, next_ids, question, answers):
        if len(next_ids) > 1:
            self._answers = answers
        else:
            self._answers = None
        self._next_ids = next_ids
        self._question = question

    def get_next_ids(self):
        return self._next_ids

    def get_question(self):
        return self._question

    def get_answers(self):
        return self._answers

    def set_next_ids(self, module_id):
        self._next_ids = module_id

    def set_question(self, question_text):
        self._question = question_text
