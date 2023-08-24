from micro_services.ApiGateWay.my_types.base_types_pb2 import Answer as EncodedAnswer
from telegram_bot.custom_types import Answer

from typing import List


async def encode_answers(answers: List[Answer]) -> List[EncodedAnswer]:
    encoded_answers = list()
    for elem in answers:
        encoded_answers.append(EncodedAnswer(module_id=int(elem.module_id), answer=elem.answer_text))
    return encoded_answers
