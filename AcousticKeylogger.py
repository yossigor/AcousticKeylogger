import asyncio
from SoundProcessor import SoundProcessor
from ModelGenerator import ModelGenerator

class AcousticKeylogger:
    def __init__(self):
        self.sound_processor = SoundProcessor()
        self.model_generator = ModelGenerator()
    async def hello(self):
        await self.model_generator.generate_model("../samples/k260_train_test","../samples/model_1")
        await self.model_generator.estimateAccuracy()