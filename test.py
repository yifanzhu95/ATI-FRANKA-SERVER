from ATI_FT import ATIDriver, ATIDriverFilter
import time
import matplotlib.pyplot as plt
import numpy as np

# print('flag')
# ft_driver = ATIDriver(hz=2000)
# ft_driver.zero_sensor()
# ft_driver.start()

# hz = 1000
# start_time = time.time()
# for i in range(4000):
#     start_time = time.time()
#     print(ft_driver.read()[2])
#     print(time.time() - start_time)
#     time.sleep(1/hz)

# ft_driver.shutdown()



## filtered version
hz = 1000
ft_driver = ATIDriverFilter(hz=hz)
ft_driver.start()
ft_driver.zero_sensor()

filtered_fts = []
raw_fts = []
start_time = time.time()
t = []
for i in range(4000):
    filtered, raw = ft_driver.read()
    filtered_fts.append(filtered)
    raw_fts.append(raw)
    
    t.append(time.time() - start_time)
    # print(f'elapsted_time {1000*(time.time() - start_time)}')
    print(filtered[2])
    time.sleep(0.1/hz)
    

ft_driver.shutdown()

#visualize
       
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