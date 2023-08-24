class Answer:
    """
    Объект представляет ответ пользователя.
    """
    
    module_id: int
    """ID модуля, на который дал ответ пользователь."""
    answer_text: str
    """Текст ответа пользователя."""

    def __init__(self, module_id: int, answer_text: str):
        self.module_id = module_id
        self.answer_text = answer_text
