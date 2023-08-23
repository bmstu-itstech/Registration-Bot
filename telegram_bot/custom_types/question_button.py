from aiogram.filters.callback_data import CallbackData


class QuestionButton(CallbackData, prefix="question_button", sep="#"):
    """
    Объект представляет коллбэк от кнопки с вопросом на стадии подтверждения введенных пользователем ответов.
    """
    
    question_id: int
    """ID вопроса, на который ссылается кнопка."""
