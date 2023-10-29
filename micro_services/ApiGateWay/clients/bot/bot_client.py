import grpc
from . import bot_pb2_grpc as pb2_grpc
from . import bot_pb2 as pb2
from . import encoder

import os
from dotenv import load_dotenv

load_dotenv()

## @brief Фукнция отправки ответов пользователя в бекенд сервиса.
# @warning Сейчас в проекте используется небезопасный канал без ssl сертификации
# @details Функция подлючается к 'DataBase microservise' по каналу gRPC, декодирует ответы
# из редиса в структуру данных, описанную в bot.proto и отправляет их методом API.
# @param chat_id Телеграмм id пользователь, чьи ответы мы записываем
# @param bot_id Id бота, с которым работает пользователь 
# @param answers Список ответов пользователя
#@code
#class Answer:
 #   """
 #   Объект представляет ответ пользователя.
 #   """
 #   
 #   module_id: int
 #  """ID модуля, на который дал ответ пользователь."""
 # answer_text: str
 #"""Текст ответа пользователя."""
 #
 #   def init(self, module_id: int, answer_text: str):
 #      self.module_id = module_id
 #      self.answer_text = answer_text
 #
#@endcode
#@param link Телеграм линк пользователя
#
#@throw GRPC-DNS-resolution-faild Возникает в случае недоступности порта или ip адреса сервера
#
#@return Вовращает ответ сервера со стурутрой вида BaseResponse описано в base_types.proto
async def push_answers(chat_id: int, bot_id: int, answers, link: str):
    
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotWorkerStub(channel)
    encoded_answers = await encoder.encode_answers(answers)
    response = await stub.SetAnswers(
        pb2.SetAnswersRequest(bot_id=bot_id, tg_chat_id=chat_id, answers=encoded_answers, telegram_link=link))

    return response

## @brief Функция получения вопроса в боте
# @param bot_id Id бота, с которым ведётся работа
# @param question_id Id модуля, с которым ведётся работа
# @throw GRPC-DNS-resolution-faild Возникает в случае недоступности порта или ip адреса сервера
# @warning Сейчас в проекте используется небезопасный канал без ssl сертификации
# @return Вовращает ответ сервера со стурутрой вида Module описано в base_types.proto
async def get_question(bot_id: int, question_id: int):
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotGetterStub(channel)
    response = await stub.GetQuestion(pb2.GetQuestionRequest(bot_id=bot_id, question_id=question_id))

    return response

## @brief Функция создания нового бота
# @param user_id Id пользователя (студенческой организации), который создаёт бота
# @param tg_token  Токен телеграмм бота, полученный из BotFather
# @param sheets_token  Токен гугл таблиц
# @param start_msg Сообщение, которое будет выводится после команды /start в боте
# @param end_msg Сообщение, которое будет выводится после завершения регистрации в боте
# @param journal Тип данных, описанный в base_types.proto - представляет собой хэш мапу из пар <id, Module> описано в base_types.proto 
# @throw GRPC-DNS-resolution-faild Возникает в случае недоступности порта или ip адреса сервера
# @warning Сейчас в проекте используется небезопасный канал без ssl сертификации
# @return Вовращает ответ сервера со стурутрой вида CreateBotResponse описано в bot.proto

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


## @brief Функция получения бота по его id 
# @param user_id Id пользователя (студенческой организации), который создаёт бота
# @param bot_id  Id бота, с которым ведётся работа
# @throw GRPC-DNS-resolution-faild Возникает в случае недоступности порта или ip адреса сервера
# @warning Сейчас в проекте используется небезопасный канал без ssl сертификации
# @return Вовращает ответ сервера со стурутрой вида BotResponse описано в bot.proto:
async def get_bot(user_id: int, bot_id: int):
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotGetterStub(channel)
    response = await stub.GetBot(pb2.GetBotRequest(bot_id=bot_id, owner=user_id))
    return response

## @brief Функция получения всех ботов 
# @throw GRPC-DNS-resolution-faild Возникает в случае недоступности порта или ip адреса сервера
# @warning Сейчас в проекте используется небезопасный канал без ssl сертификации
# @return Вовращает ответ сервера со стурутрой вида BotsResponse описано в bot.proto:
async def get_bots():
    channel = grpc.aio.insecure_channel(os.getenv('DATABASE_CONNECTION'))
    stub = pb2_grpc.BotGetterStub(channel)
    response = await stub.GetAllBots(pb2.GetBotRequest())

    return response
