# python -m grpc_tools.protoc -I./protos --python_out=clients/bot --pyi_out=clients/bot --grpc_python_out=clients/bot protos/bot.proto
# python -m grpc_tools.protoc -I./protos --python_out=services/authorizer --grpc_python_out=services/authorizer protos/authorization.proto
#  python -m grpc_tools.protoc -I./protos --python_out=my_types --pyi_out=my_types/ --grpc_python_out=my_types/ protos/base_types.proto
import asyncio

from clients.bot.bot_client import *
from my_types.base_types_pb2 import Answer
if __name__ == "__main__":
    answer = Answer()
    answer.module_id = 1
    answer.answer_text = "122"

    answer1 = Answer()
    answer1.module_id = 2
    answer1.answer_text = 'true'

    asyncio.get_event_loop().run_until_complete(set_answers(4747, 40, [answer,answer1]))
