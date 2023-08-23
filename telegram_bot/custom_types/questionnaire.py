from aiogram.filters.state import State, StatesGroup


class Questionnaire(StatesGroup):
    """
    Объект представляет состояние прохождения анкеты.
    """

    in_process = State()
    """Показывает, что анкета в стадии прохождения."""
    on_approval = State()
    """Показывает, что анкета в стадии одобрения пользователем."""
    completed = State()
    """Показывает, что анкета заполнена пользователем и повторное заполнение не допускается."""
