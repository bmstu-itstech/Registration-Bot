import grpc
from . import bot_pb2_grpc as pb2_grpc
from . import bot_pb2 as pb2
from . import encoder

import os
from dotenv import load_dotenv

load_dotenv()


async def push_answers(chat_id: int, bot_id: int, answers, link: str):
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotWorkerStub(channel)
    encoded_answers = await encoder.encode_answers(answers)
    response = await stub.SetAnswers(
        pb2.SetAnswersRequest(bot_id=bot_id, tg_chat_id=chat_id, answers=encoded_answers, telegram_link=link))

    return response


async def get_question(bot_id: int, question_id: int):
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotGetterStub(channel)
    response = await stub.GetQuestion(pb2.GetQuestionRequest(bot_id=bot_id, question_id=question_id))

    return response


async def create_new_bot_asker(user_id: int, journal, tg_token: str, sheets_token: str, start_msg: str, end_msg: str):
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))

    try:
        stub = pb2_grpc.BotWorkerStub(channel)
        response = await stub.CreateBot(
            pb2.CreateBotRequest(from_user=user_id, journal=journal, start_message=start_msg,
                                 tg_token=tg_token, sheets_token=sheets_token, end_message=end_msg))
        return response

    except Exception as ex:
        print(ex)
        return None



async def get_bot(user_id: int, bot_id: int):
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotGetterStub(channel)
    response = await stub.GetBot(pb2.GetBotRequest(bot_id=bot_id, owner=user_id))
    return response


async def get_bots():
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotGetterStub(channel)
    response = await stub.GetAllBots(pb2.GetBotRequest())

    return response
