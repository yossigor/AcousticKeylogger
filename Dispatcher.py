import asyncio
import numpy as np


dispatcher_threshold = 80
dispatcher_min_interval = 14000
dispatcher_window_size = 100
dispatcher_step_size = 1
dispatcher_persistence = True
    

class Dispatcher:
    def __init__(self):
        pass
        
    def offline(data):
        print("DISPATCHER:processing data...")
        rem = len(data) % 441
        data = np.array(data[:len(data) - rem])
        minimum_interval = dispatcher_min_interval
        sample_length = (44100 * dispatcher_window_size) / 1000
        persistence = dispatcher_persistence

        peaks = []
        for x in range(0, len(data) - 440):
            peaks.append(np.sum(np.absolute(np.fft.fft(data[x:x + 440]))))
        