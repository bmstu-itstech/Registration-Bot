import grpc
import clients.bot.bot_pb2_grpc as pb2_grpc
import clients.bot.bot_pb2 as pb2

import conf


# TODO
# не грузиться ответ в setAnswers
# question_type должен быть рабочим
# структура ansewers
async def set_answers(chat_id: int, bot_id: int, answers_list):
    with grpc.insecure_channel(conf.DATABASE_CONNECTION) as channel:
        stub = pb2_grpc.BotWorkerStub(channel)
        response = await stub.SetAnswers(pb2.SetAnswersRequest(bot_id=bot_id, tg_chat_id=chat_id, answers=answers_list))

        return response


async def get_question_by_id(bot_id: int, question_id: int):
    with grpc.insecure_channel(conf.DATABASE_CONNECTION) as channel:
        stub = pb2_grpc.BotGetterStub(channel)
        response = await stub.GetQuestion(pb2.GetQuestionRequest(bot_id=bot_id, question_id=question_id))

        return response


async def create_new_bot_asker(user_id: int, journal):
    with grpc.insecure_channel(conf.DATABASE_CONNECTION) as channel:
        stub = pb2_grpc.BotWorkerStub(channel)
        response = await stub.CreateBot(pb2.CreateBotRequest(from_user=user_id, journal=journal))

        return response
