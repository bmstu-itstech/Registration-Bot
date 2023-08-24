from typing import List
from telegram_bot.custom_types import Answer


async def pack_answers(answers_dict: dict) -> List[Answer]:
    answers = list()
    for key, item in answers_dict.items():
        answers.append(Answer(key, item))
    return answers
