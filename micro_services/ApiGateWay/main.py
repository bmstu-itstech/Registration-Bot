# python -m grpc_tools.protoc -I./protos --python_out=clients/bot --pyi_out=clients/bot --grpc_python_out=clients/bot protos/bot.proto
# python -m grpc_tools.protoc -I./protos --python_out=services/authorizer --grpc_python_out=services/authorizer protos/authorization.proto
#  python -m grpc_tools.protoc -I./protos --python_out=my_types --pyi_out=my_types/ --grpc_python_out=my_types/ protos/base_types.proto
import asyncio

from clients.bot.bot_client import *
from my_types.base_types_pb2 import Answer

if __name__ == "__main__":
    #asyncio.get_event_loop().run_until_complete(get_bots())
    asyncio.get_event_loop().run_until_complete(get_bot(bot_id=64,user_id=2))

    # answer = Answer()
    # answer.module_id = 1
    # answer.ansewer_text = "Митрошкин Алексей Антонович"
    #
    # answer1 = Answer()
    # answer1.module_id = 2
    # answer1.ansewer_text = 'true'
    #
    # asyncio.get_event_loop().run_until_complete(set_answers(4747, 64, [answer, answer1]))
