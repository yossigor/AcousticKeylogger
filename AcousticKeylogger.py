import asyncio
import pickle #used to save objects to a file
import os
import matplotlib.pyplot as plt
import itertools
import functools
from concurrent.futures import ProcessPoolExecutor
from SoundProcessor import SoundProcessor
from ModelGenerator import ModelGenerator
from Classifier import Classifier


NUMBER_OF_WORKERS = 4


class AcousticKeylogger:
    def __init__(self,config):
        self.config = config
        self.sound_processor = SoundProcessor()
        self.model_generator = ModelGenerator(config)
    async def classify_and_check_accuracy(self,model_file,target_file,truth,top_n):
        classifier = await self.load_model_from_disk(model_file)
        predictions = await classifier.classify(target_file)
        print(predictions);
        accuracy = await classifier.check_accuracy(predictions,top_n,truth)
        print('Top {} accuracy: {}'.format(top_n,accuracy))
        return accuracy
    async def hello(self):
        clf = await self.model_generator.generate_model("../samples/k260_train_test_accuracy","../samples/model_1")
        # await self.model_generator.estimateAccuracy()
        classifier = Classifier(clf,self.config)
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
        model_generator = ModelGenerator(self.config)
        classifier = Classifier(await model_generator.generate_model(training_folder,model_output),self.config)
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
    async def get_smart_dictionary(self,passwords_recording_folder,dictionary_output,model_file):
        target_files = []
        if os.path.isdir(passwords_recording_folder):
            for r, d, fs in os.walk(passwords_recording_folder):
                for fn in fs:
                    f1 = os.path.abspath(os.path.join(r, fn))
                    ext = os.path.splitext(f1)[1]
                    if ext == '.wav':
                        target_files.append(f1)
        print("Target files: {}".format(target_files))
        classifier = await self.load_model_from_disk(model_file)
        executor = ProcessPoolExecutor(max_workers=NUMBER_OF_WORKERS)
        classification_tasks = []
        for target in target_files:
            classification_tasks.append(classifier.classify(target))
        predictions_output = await asyncio.gather(*classification_tasks)
        predictions_flatted = []
        for target in predictions_output:
            for prediction in target:
                predictions_flatted.append(prediction)
        histograms = dict()
        for prediction in predictions_flatted:
            index = prediction[0]
            list_of_keys = prediction[1]
            if index in histograms:
                pass
            else:
                histograms[index] = dict()
            w = 5;
            for key in list_of_keys:
                if key in histograms[index]:
                    histograms[index][key] += w
                else:
                    histograms[index][key] = w
                if w > 1:
                    w -=1
        smart_dictionary_data = [];
        for letter in histograms:
            items = [];
            for key,count in histograms[letter].items():
                items.append((key,count))
            items.sort(key = lambda x:x[1])
            items.reverse()
            smart_dictionary_data.append(items[:5])
            #plotting
            names = list([x[0] for x in items[:10]])
            values = list([x[1] for x in items[:10]])
            fig, axs = plt.subplots(1, 1, figsize=(9, 3), sharey=True)
            axs.bar(names, values)
            fig.suptitle('Categorical Plotting')
            plt.show()
        smart_dict = list(map(lambda tuple:list(tuple) ,list(itertools.product(*smart_dictionary_data))))
        smart_dict = list(map(lambda list:(list,functools.reduce(lambda a,b: a+b[1], list, 0)) ,smart_dict))
        smart_dict.sort(key = lambda guess: guess[1])
        smart_dict.reverse()
        output_file = open(dictionary_output,'w')
        for guess in smart_dict:
            output_file.write(''.join((list(map(lambda tuple: tuple[0],guess[0]))))+'\n')
        output_file.close()
    async def sound_preprocess(self,training_folder,output_folder):
        await self.sound_processor.time_stretch_train_folder(training_folder,output_folder,self.config['time_stretch'])