#python -m grpc_tools.protoc -I./protos --python_out=services/baseTypes --grpc_python_out=services/baseTypes protos/base_types.proto
#python -m grpc_tools.protoc -I./protos --python_out=services/bot_service --grpc_python_out=services/bot_service protos/bot.proto
import grpc
from conf import *

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))

    connection = f'{SERVER_IP}:{SERVER_PORT}'

    if DEBAG:
        connection = f"{DEBAG_SERVER_IP}:{DEBAG_SERVER_PORT}"
    server.add_insecure_port(connection)
    server.start()

    print(f"Server started at {connection}")
    server.wait_for_termination()