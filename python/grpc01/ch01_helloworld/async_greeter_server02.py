import asyncio
import logging
import sys
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

port = '50051'


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    async def SayHello(self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext) -> helloworld_pb2.HelloResponse:
        return helloworld_pb2.HelloResponse(message="hello " + request.name)

    async def SayHelloAgain(self, request: helloworld_pb2.HelloRequest, context: grpc.ServicerContext) -> helloworld_pb2.HelloResponse:
        return helloworld_pb2.HelloResponse(message="hello again " + request.name)


async def server_demo() -> None:
    server = grpc.aio.server()
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    await server.start()
    print("Server started, listening on : " + port)
    await server.wait_for_termination()


async def client_demo() -> None:
    async with grpc.aio.insecure_channel("localhost:" + port) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = await stub.SayHello(helloworld_pb2.HelloRequest(name="liu"))
        print("Greeter client received " + response.message)
        response = await stub.SayHelloAgain(helloworld_pb2.HelloRequest(name="liu"))
        print("Greeter client received " + response.message)


if __name__ == "__main__":
    if sys.argv[1] == "server":
        asyncio.run(server_demo())
    else:
        asyncio.run(client_demo())
