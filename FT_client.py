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
    ## filtered version
    hz = 2000
    ft_driver = FTClient('http://172.16.0.1:8080')
    ft_driver.zero_ft_sensor()
    ft_driver.start_ft_sensor()
    filtered_fts = []
    raw_fts = []
    for i in range(4000):
        start_time = time.time()
        filtered, raw = ft_driver.read_ft_sensor()
        filtered_fts.append(filtered)
        raw_fts.append(raw)
        time.sleep(1/hz)

    ft_driver.shutdown_ft_sensor()

    #visualize
    t = np.linspace(0,2,4000)        
    plt.figure(figsize=(10, 5))
    plt.plot(t, np.array(raw_fts)[:,2], label='Noisy Signal Fz ')
    plt.plot(t, np.array(filtered_fts)[:,2], label='Filtered Signal Fz', linewidth=2)
    plt.title("Butterworth Low-Pass Filter")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    ##
    # ft_driver = FTClient('http://172.16.0.1:8080')
    # ft_driver.zero_ft_sensor()
    # ft_driver.start_ft_sensor()
    # for i in range(100):
    #     start_time = time.time()
    #     print(ft_driver.read_ft_sensor())
    #     time.sleep(0.1)
    # ft_driver.shutdown_ft_sensor()