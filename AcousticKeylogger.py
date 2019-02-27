import asyncio
import pickle #used to save objects to a file
from SoundProcessor import SoundProcessor
from ModelGenerator import ModelGenerator
from Classifier import Classifier



class AcousticKeylogger:
    def __init__(self):
        self.sound_processor = SoundProcessor()
        self.model_generator = ModelGenerator()
    async def hello(self):
        clf = await self.model_generator.generate_model("../samples/k260_train_test_accuracy","../samples/model_1")
        # await self.model_generator.estimateAccuracy()
        classifier = Classifier(clf)
        predictions = await classifier.classify('../samples/k260_target/target_3.wav')
        print(predictions);
        truth = ['o','n','e','_','r','i','n','g','_','t','o','_','r','u','l','e','_'
            ,'t','h','e','m','_','a','l','l','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'f','i','n','d','_','t','h','e','m','_','o','n','e','_','r','i','n','g','_','t','o','_'
            ,'b','r','i','n','g','_','t','h','e','m','_','a','l','l','_','a','n','d','_','i','n','_'
            ,'t','h','e','_','d','a','r','k','n','e','s','s','_','b','i','n','d','_','t','h','e','m']
        top_n = 5
        accuracy = await classifier.check_accuracy(predictions,top_n,truth)
        print('Top {} accuracy: {}'.format(top_n,accuracy))
    async def write_model_to_disk(self,training_folder,model_output):
        model_generator = ModelGenerator()
        classifier = Classifier(await model_generator.generate_model(training_folder,model_output))
        filehandler = open(model_output, 'wb') 
        pickle.dump(classifier, filehandler)
        print("Model written to {}".format(model_output));
    async def load_model_from_disk(self,model_file) -> Classifier:
        filehandler = open(model_file, 'rb') 
        classifier = pickle.load(filehandler)
        return classifier
    async def print_predictions(self,predictions):
        for prediction in predictions:
            idx = prediction[0]
            sugessted_keys = prediction[1]
            print("{} - {}".format(idx,sugessted_keys))
    async def classification_attack(self,target_file,model_file):
        classifier = await self.load_model_from_disk(model_file)
        predictions = await classifier.classify(target_file)
        await self.print_predictions(predictions)
