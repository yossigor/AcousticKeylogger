import asyncio
import numpy as np


class Dispatcher:
    def __init__(self):
        self.dispatcher_threshold = 80
        self.dispatcher_min_interval = 14000
        self.dispatcher_window_size = 100
        self.dispatcher_step_size = 1
        self.dispatcher_persistence = True
    
    def offline(wav_data):
        print("DISPATCHER:processing data...")
        