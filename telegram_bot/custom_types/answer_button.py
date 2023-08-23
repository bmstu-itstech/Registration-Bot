from aiogram.filters.callback_data import CallbackData
from typing import Optional


class AnswerButton(CallbackData, prefix="answer_button", sep="#"):
    """
    Объект представляет коллбэк от кнопки с ответом на вопрос.
    """

    next_id: Optional[int]
    """ID вопроса, на который ведет кнопка в случае ее нажатия пользователем."""
    answer: str
    """Текст ответа."""
