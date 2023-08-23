import asyncio

import web_api_rpc.web_api_pb2 as pb2
import web_api_rpc.web_api_pb2_grpc as p2b_grpc

import clients.bot.bot_client as bot


class DataSenderService(p2b_grpc.DataSenderServicer):
     def Create_Bot(self, request, context):
        print("Create bot request")
        resp = asyncio.new_event_loop().run_until_complete(bot.create_new_bot_asker(user_id=request.from_user,journal=request.journal))
        return resp