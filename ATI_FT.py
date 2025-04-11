import nidaqmx
import numpy as np
import time, copy
import pickle
import threading
from threading import Thread, Lock, RLock
from scipy.signal import butter, filtfilt
from collections import deque

calmat = [[-0.009588917717, 0.21333759651, -0.211067259312, -7.340359210968, 0.099111407995, 7.244591712952],\
    [0.173573523760, 8.756484985352, -0.151811018586, -4.205108642578, -0.012327974662, -4.241057395935],\
    [13.291530609131, -0.411136031151, 13.170610427856, -0.014774517156, 13.120358467102, -0.166001349688],\
    [0.002582752146, 0.001690946170, -0.384541809559, -0.001996719977, 0.374509602785, -0.003547623521],\
    [0.443082749844, -0.013428002596, -0.220946237445, 0.002811806975, -0.221077233553, -0.000530479301],\
    [-0.004413546994, -0.238919422030, -0.008464409970, -0.232588291168, -0.001325184712, -0.229158148170]]

class ATIDriver:
    def __init__(self, hz = 100.) -> None:
        self.hz = hz 
        self.offset = np.zeros(6)
        self.reading = np.zeros(6)
        self._loopLock = RLock()
        #Daq board
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai4")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai5")


    def start(self):
        controlThread = threading.Thread(target = self._loop)
        self.shut_down_flag = False
        controlThread.start()
        print("ATIDriver:started")
        return True

    def zero_sensor(self, N = 20):
        test_total = self.task.read()
        for testNum in range(N):
            test = self.task.read()
            for item in range(len(test_total)):
                test_total[item] = test_total[item]+test[item]
        zeros = [x/(N+1) for x in test_total]
        self.offset = np.array(zeros)

    def _loop(self):
        """main control thread, synchronizing all components
        in each loop,states are updated and new commands are issued
        """
        while not self.shut_down_flag:
            self._loopLock.acquire()
            data = np.array(self.task.read())
            for itemNum in range(len(data)):
                data[itemNum] = data[itemNum] - self.offset[itemNum]
            self.reading = np.transpose(np.matmul(calmat, np.transpose(data)))
            self._loopLock.release()
            time.sleep(1./self.hz)
        
        print('ATIDriver: Exiting')

    def read(self):
        return copy.copy(self.reading.tolist())

    def shutdown(self):
        self._loopLock.acquire()
        self.shut_down_flag = True
        self._loopLock.release()



# Apply the filter
def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order)
    y = filtfilt(b, a, data)
    return y


class ATIDriverFilter:
    def __init__(self, hz = 2000., cutoff = 100., history_length = 100) -> None:
        self.hz = hz 
        self.offset = np.zeros(6)
        self.reading = np.zeros(6)
        self._loopLock = RLock()

        #Low-pass filter
        nyq = 0.5 * hz  # Nyquist frequency
        normal_cutoff = cutoff / nyq
        self.b, self.a = butter(4, normal_cutoff, btype='low', analog=False)

        #history
        self.history = deque(maxlength=history_length)
        self.history_length = history_length
        #Daq board
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai4")
        self.task.ai_channels.add_ai_voltage_chan("Dev1/ai5")


    def start(self):
        controlThread = threading.Thread(target = self._loop)
        self.shut_down_flag = False
        controlThread.start()
        self.fill_history()
        print("ATIDriver:started")
        return True

    def fill_history(self):
        while len(self.history) < self.history_length:
            data = np.array(self.task.read())
            for itemNum in range(len(data)):
                data[itemNum] = data[itemNum] - self.offset[itemNum]
            self.reading = np.transpose(np.matmul(calmat, np.transpose(data)))
            self.history.append(self.reading)
            time.sleep(1./self.hz)

    def zero_sensor(self, N = 20):
        test_total = self.task.read()
        for testNum in range(N):
            test = self.task.read()
            for item in range(len(test_total)):
                test_total[item] = test_total[item]+test[item]
        zeros = [x/(N+1) for x in test_total]
        self.offset = np.array(zeros)

    def _loop(self):
        """main control thread, synchronizing all components
        in each loop,states are updated and new commands are issued
        """
        while not self.shut_down_flag:
            self._loopLock.acquire()
            data = np.array(self.task.read())
            for itemNum in range(len(data)):
                data[itemNum] = data[itemNum] - self.offset[itemNum]
            self.reading = np.transpose(np.matmul(calmat, np.transpose(data)))
            self.history.append(self.reading)
            self._loopLock.release()
            time.sleep(1./self.hz)
        
        print('ATIDriver: Exiting')

    def read(self):
        #return copy.copy(self.reading.tolist())
        return filtfilt(self.b, self.a, np.array(self.history).T)[:,-1].tolist(), self.history[-1].tolist()

    def shutdown(self):
        self._loopLock.acquire()
        self.shut_down_flag = True
        self._loopLock.release()
