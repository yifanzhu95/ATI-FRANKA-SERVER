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
        self.shut_down = False

    def test(self):
        return self.s.test()


if __name__=="__main__":
    ft_arm_driver = FTClient('http://localhost:8080')
    print(ft_arm_driver.test())
