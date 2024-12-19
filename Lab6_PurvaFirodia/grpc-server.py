# import grpc
# from concurrent import futures
# import service_pb2
# import service_pb2_grpc
# from PIL import Image
# import io
# import base64

# class MyService(service_pb2_grpc.MyServiceServicer):
#     def Add(self, request, context):
#         return service_pb2.addReply(sum=request.a + request.b)

#     def DotProduct(self, request, context):
#         dot_product = sum(x * y for x, y in zip(request.a, request.b))
#         return service_pb2.dotProductReply(dotproduct=dot_product)

#     def JsonImage(self, request, context):
#         img_data = base64.b64decode(request.img)
#         img = Image.open(io.BytesIO(img_data))
#         return service_pb2.imageReply(width=img.size[0], height=img.size[1])

#     def RawImage(self, request, context):
#         img = Image.open(io.BytesIO(request.img))
#         return service_pb2.imageReply(width=img.size[0], height=img.size[1])

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
#     server.add_insecure_port('[::]:50051')
#     server.start()
#     server.wait_for_termination()

# if __name__ == '__main__':
#     serve()



import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
from PIL import Image
import io
import base64

class MyService(service_pb2_grpc.MyServiceServicer):
    def Add(self, request, context):
        return service_pb2.addReply(sum=request.a + request.b)

    def DotProduct(self, request, context):
        dot_product = sum(x * y for x, y in zip(request.a, request.b))
        return service_pb2.dotProductReply(dotproduct=dot_product)

    def JsonImage(self, request, context):
        img_data = base64.b64decode(request.img)
        img = Image.open(io.BytesIO(img_data))
        return service_pb2.imageReply(width=img.size[0], height=img.size[1])

    def RawImage(self, request, context):
        img = Image.open(io.BytesIO(request.img))
        return service_pb2.imageReply(width=img.size[0], height=img.size[1])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
