import asyncio
from SoundProcessor import SoundProcessor
from ModelGenerator import ModelGenerator
from Classifier import Classifier

class AcousticKeylogger:
    def __init__(self):
        self.sound_processor = SoundProcessor()
        self.model_generator = ModelGenerator()
    async def hello(self):
        clf = await self.model_generator.generate_model("../samples/k260_train_test","../samples/model_1")
        # await self.model_generator.estimateAccuracy()
        classifier = Classifier(clf)
        predictions = await classifier.classify('../samples/k260_target/target_3.wav')
        print(predictions);
        truth = ['o','n','e','_','r','i','n','g','_','t','o','_','r','u','l','e','_'
            ,'t','h','e','m','_','a','l','l','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'f','i','n','d','_','t','h','e','m','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'b','r','i','n','g','_','t','h','e','m','_','a','l','l','_','a','n','d','_','i','n','_'
            ,'t','h','e','_','d','a','r','k','n','e','s','s','_','b','i','n','d','_','t','h','e','m']
        accuracy = await classifier.check_accuracy(predictions,5,truth)
        