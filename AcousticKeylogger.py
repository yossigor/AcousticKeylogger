import asyncio
from SoundProcessor import SoundProcessor
from ModelGenerator import ModelGenerator

class AcousticKeylogger:
    def __init__(self):
        self.sound_processor = SoundProcessor()
        self.model_generator = ModelGenerator()
    async def hello(self):
        print("hello,")
        await self.sound_processor.hello()
        await self.model_generator.hello()