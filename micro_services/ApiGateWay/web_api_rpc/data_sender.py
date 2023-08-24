import asyncio

import micro_services.ApiGateWay.web_api_rpc.web_api_pb2 as pb2
import micro_services.ApiGateWay.web_api_rpc.web_api_pb2_grpc as p2b_grpc
import micro_services.ApiGateWay.clients.bot.bot_client as bot
from telegram_bot.bot_launcher import run_instance


class DataSenderService(p2b_grpc.DataSenderServicer):
    async def Create_Bot(self, request, context):
        resp = await bot.create_new_bot_asker(user_id=request.from_user, journal=request.journal)
        await run_instance(resp.bot_id)
        return resp
