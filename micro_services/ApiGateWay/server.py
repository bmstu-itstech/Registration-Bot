import os

from web_api_rpc.data_sender import DataSenderService
import grpc
from web_api_rpc import web_api_pb2_grpc
from web_api_rpc import web_api_pb2
from concurrent import futures


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    web_api_pb2_grpc.add_DataSenderServicer_to_server(DataSenderService(), server)
    conn = os.getenv('SERVER_IP')

    server.add_insecure_port(conn)
    server.start()
    print(f"Server started at {conn}")
    server.wait_for_termination()
