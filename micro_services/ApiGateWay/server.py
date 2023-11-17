import os

from micro_services.ApiGateWay.web_api_rpc.data_sender import DataSenderService
from grpc import aio
from micro_services.ApiGateWay.web_api_rpc import web_api_pb2_grpc
from micro_services.ApiGateWay.web_api_rpc import web_api_pb2
from concurrent import futures

## @brief Функция запуска сервера gRPC.
#  Создаёт объект сервера и инициализирует сервисы, описанные в контрактах gRPC
#  @see @ref data_sender.DataSenderService
async def serve():
    server = aio.server()
    web_api_pb2_grpc.add_DataSenderServicer_to_server(DataSenderService(), server)
    conn = os.getenv('SERVER_IP')

    server.add_insecure_port(conn)
    await server.start()
    print(f"Server started at {conn}")
    await server.wait_for_termination()
