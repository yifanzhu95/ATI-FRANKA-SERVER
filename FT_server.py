from xmlrpc.server import SimpleXMLRPCServer
from ATI_FT import ATIDriver

ip_address = 'localhost'
port = 8080

server = SimpleXMLRPCServer((ip_address,port), logRequests=False)
print(f"Listening on port {port}...")
server.register_introspection_functions()

def xmlrpcMethod(name):
    """
    Decorator that registers a function to the xmlrpc server under the given name.
    """
    def register_wrapper(f):
        server.register_function(f, name)
        return f
    return register_wrapper

## Franka Driver

# ATI Driver
global ft_sensor
ft_sensor = ATIDriver()

# ATI functions 
@xmlrpcMethod("zero_ft_sensor")
def zero_ft_sensor():
    global ft_sensor
    ft_sensor.zero_sensor()

@xmlrpcMethod("start_ft_sensor")
def start_ft_sensor():
    global ft_sensor
    ft_sensor.start()

@xmlrpcMethod("read_ft_sensor")
def read_ft_sensor():
    global ft_sensor
    return ft_sensor.read()

@xmlrpcMethod("shutdown_ft_sensor")
def shutdown_ft_sensor():
    global ft_sensor
    ft_sensor.shutdown()



print('Server Created')
##run server
server.serve_forever()