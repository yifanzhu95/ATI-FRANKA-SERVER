from xmlrpc.server import SimpleXMLRPCServer
from franka_python_controller import FrankaController
from franka_python_controller.motionUtils import GlobalCollisionHelper
from klampt import RobotModel, vis
from klampt import WorldModel,RobotModel
from klampt.model import ik,collide
from klampt.math import so3, se3, vectorops as vo

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
world_fn = "./models/franka_world.xml"
EE_link = 'tool_link'
world = WorldModel()
world.readFile(world_fn)
robot_model = world.robot(0)
collider = collide.WorldCollider(world)
collision_checker = GlobalCollisionHelper(robot_model, collider)
params = {'address': "172.16.0.2"} ## TBD, joint stiffness can also be set here 
# 'impedance', [3000, 3000, 3000, 2500, 2500, 2000, 2000] ## default

# controller instance
global controller
controller = FrankaController(name = 'Franka', robot_model = robot_model, EE_link = EE_link, \
    collision_checker = collision_checker, params = params)

# Franka interface
@xmlrpcMethod("initialize")
def initialize():
    global controller
    controller.initialize()

@xmlrpcMethod("start")
def start():
    global controller
    controller.start()

@xmlrpcMethod("shutdown")
def shutdown():
    global controller
    controller.close()

@xmlrpcMethod("get_joint_config")
def get_joint_config():
    global controller
    return controller.get_joint_config()

@xmlrpcMethod("get_joint_velocity")
def get_joint_velocity():
    global controller
    return controller.get_joint_velocity()

@xmlrpcMethod("get_joint_torques")
def get_joint_torques():
    global controller
    return controller.get_joint_torques()

@xmlrpcMethod("get_EE_transform")
def get_EE_transform(tool_center):
    global controller
    return controller.get_EE_transform(tool_center)

@xmlrpcMethod("get_EE_velocity")
def get_EE_velocity():
    global controller
    return controller.get_EE_velocity()

@xmlrpcMethod("get_EE_wrench")
def get_EE_wrench():
    global controller
    return controller.get_EE_wrench()

@xmlrpcMethod("set_joint_config")
def set_joint_config(q):
    global controller
    controller.set_joint_config(q, {})

@xmlrpcMethod("set_EE_transform")
def set_EE_transform(T):
    global controller
    controller.set_EE_transform(T, {})

@xmlrpcMethod("set_EE_velocity")
def set_EE_velocity(v):
    global controller
    controller.set_EE_velocity(v, {})

    

print('Server Created')
##run server
server.serve_forever()