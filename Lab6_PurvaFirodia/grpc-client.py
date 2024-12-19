import grpc
import service_pb2
import service_pb2_grpc
import random
import base64
import sys
from time import perf_counter

# Get the command-line arguments
addr = sys.argv[1]
endpoint = sys.argv[2]
num_tests = int(sys.argv[3])

# Load the image file
img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()

# Open a gRPC channel
channel = grpc.insecure_channel(addr)

def doAdd(stub):
    """Performs addition via gRPC."""
    timer1_start = perf_counter()
    for i in range(num_tests):
        number = service_pb2.addMsg(a=5, b=4)
        resp = stub.Add(number)
        print(f"Addition result: {resp.sum}")
    timer1_stop = perf_counter()
    total = timer1_stop - timer1_start
    # avg = total / num_tests
    print(f"Time for addition: {total}")

def doRawImage(stub):
    """Sends raw image data to the gRPC server."""
    timer1_start = perf_counter()
    for i in range(num_tests):
        number = service_pb2.rawImageMsg(img=img)
        resp = stub.RawImage(number)
        print(f"Image response: {resp.width}, {resp.height}")
    timer1_stop = perf_counter()
    total = timer1_stop - timer1_start
    # avg = total / num_tests
    print(f"Time for raw image: {total}")

def doDotProduct(stub):
    """Performs dot product operation via gRPC."""
    timer1_start = perf_counter()  # Start timing
    for i in range(num_tests):
        a = [random.random() for _ in range(100)]
        b = [random.random() for _ in range(100)]
        response = stub.DotProduct(service_pb2.dotProductMsg(a=a, b=b))
        print(f"Dot Product: {response.dotproduct}")
    timer1_stop = perf_counter()  # Stop timing

    total = timer1_stop - timer1_start
    # avg = total / num_tests
    print(f"Time for dot product: {total}")  # Print average time

def doJsonImage(stub):
    """Sends JSON-encoded image data to the gRPC server."""
    timer1_start = perf_counter()  # Start timing
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    for i in range(num_tests):  # Loop for multiple tests
        response = stub.JsonImage(service_pb2.jsonImageMsg(img=encoded_image))
        print(f"Image dimensions: {response.width}x{response.height}")

    timer1_stop = perf_counter()  # Stop timing
    total = timer1_stop - timer1_start
    # avg = total / num_tests
    print(f"Average time for JSON image: {total}")  # Print average time

def run():
    """Selects the appropriate function based on the endpoint provided."""
    stub = service_pb2_grpc.MyServiceStub(channel)
    
    if endpoint == 'add':
        doAdd(stub)
    elif endpoint == 'rawimage':
        doRawImage(stub)
    elif endpoint == 'dotproduct':
        doDotProduct(stub)
    elif endpoint == 'jsonimg':
        doJsonImage(stub)
    else:
        print(f"Unknown endpoint: {endpoint}")

if __name__ == '__main__':
    run()


