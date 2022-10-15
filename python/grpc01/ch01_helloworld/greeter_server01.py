from concurrent import futures
import logging
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import sys

port = '50051'


class GreeterServer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloResponse(message="hello {}".format(request.name))

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloResponse(message="hello again  {}".format(request.name))


def server_demo():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on : " + port)
    server.wait_for_termination()


def client_demo():
    with grpc.insecure_channel("localhost:" + port) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="liu"))
        print("Greeter client received " + response.message)
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name="liu"))
        print("Greeter client received " + response.message)


if __name__ == "__main__":
    if sys.argv[1] == "server":
        server_demo()
    else:
        client_demo()
