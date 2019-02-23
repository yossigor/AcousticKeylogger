import asyncio
from SoundProcessor import SoundProcessor
from ModelGenerator import ModelGenerator
from Classifier import Classifier

class AcousticKeylogger:
    def __init__(self):
        self.sound_processor = SoundProcessor()
        self.model_generator = ModelGenerator()
        self.classifier = Classifier()
    async def hello(self):
        await self.model_generator.generate_model("../samples/k260_train_test","../samples/model_1")