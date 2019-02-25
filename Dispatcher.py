import asyncio
import numpy as np
import math


dispatcher_threshold = 80
dispatcher_min_interval = 14000
dispatcher_window_size = 100
dispatcher_step_size = 1
dispatcher_persistence = True
    

class Dispatcher:
    def __init__(self):
        pass
        
    def rms(series):
        return math.sqrt(sum(series ** 2) / series.size)

    def normalize(series):
        return series / Dispatcher.rms(series)
        
    def offline(data):
        print("DISPATCHER:processing data...")
        output = []
        rem = len(data) % 441
        data = np.array(data[:len(data) - rem])
        minimum_interval = dispatcher_min_interval
        sample_length = (44100 * dispatcher_window_size) / 1000
        persistence = dispatcher_persistence

        peaks = []
        for x in range(0, len(data) - 440):
            peaks.append(np.sum(np.absolute(np.fft.fft(data[x:x + 440]))))
        peaks = np.array(peaks)
        tau = np.percentile(peaks, dispatcher_threshold)
        x = 0
        events = []
        step = dispatcher_step_size
        past_x = - minimum_interval - step
        idx = 0
        while x < peaks.size:
            if peaks[x] >= tau:
                if x - past_x >= minimum_interval:
                    # It is a keypress event (maybe)
                    keypress = Dispatcher.normalize(data[x:x + int(sample_length)])
                    past_x = x
                    output.append([idx, keypress])
                    idx += 1
                    events.append(keypress)
                x = past_x + minimum_interval
            else:
                x += step
        return output
        