from xmlrpc.client import ServerProxy
from threading import Thread, Lock
import threading
import time
import os
import numpy as np
dirname = os.path.dirname(__file__)

class FTClient:
    def __init__(self, address = 'http://127.0.0.1:8080'):
        self.s = ServerProxy(address)
        #self.shut_down = False

    def zero_ft_sensor(self):
        self.s.zero_ft_sensor()

    def start_ft_sensor(self):
        self.s.start_ft_sensor()

    def read_ft_sensor(self):
        return self.s.read_ft_sensor()

    def shutdown_ft_sensor(self):
        self.s.shutdown_ft_sensor()

if __name__=="__main__":
    ft_arm_driver = FTClient('http://127.0.0.1:8080')
    ft_arm_driver.zero_ft_sensor()
    ft_arm_driver.start_ft_sensor()
    for i in range(100):
        start_time = time.time()
        time.sleep(0.1)
    ft_arm_driver.shutdown_ft_sensor()