import asyncio
import numpy as np
import operator
import functools
from Listener import Listener
from Dispatcher import Dispatcher
from concurrent.futures import ProcessPoolExecutor

NUMBER_OF_WORKERS = 4

class Worker:
    def __init__(self):
        pass
    def work(clf,data_for_worker,n_preds):
        output = []
        for idx, sample in data_for_worker:
            if idx < 0:
                break
            prediction = clf.predict_proba(sample.reshape(1, -1))[0]
            values = [x[0] for x in
                    sorted([(clf.classes_[x], val) for x, val in enumerate(prediction) if val != 0.0],
                            key=lambda _x: _x[1], reverse=True)]
            output.append((idx, values[:n_preds]))
        return output

class Classifier:
    def __init__(self,clf,config):
        self.clf = clf
        self.config = config
    async def process_file(self,file_path):
        print('processing {}'.format(file_path))
        listener_output = Listener.read_wav_file(file_path)
        print('Listening completed')
        dispatcher_output = Dispatcher.offline(listener_output,self.config)
        print('Dispatching completed')
        return dispatcher_output;
    async def classify(self,file_path):
        data = await self.process_file(file_path)
        print('File processing completed')
        executor = ProcessPoolExecutor(max_workers=NUMBER_OF_WORKERS)
        working_tasks = []
        for data_for_worker in np.array_split(data,NUMBER_OF_WORKERS):
            working_tasks.append(asyncio.get_running_loop().run_in_executor(
                executor,Worker.work,self.clf,data_for_worker,10))
        working_output = await asyncio.gather(*working_tasks)
        return functools.reduce(operator.iconcat, working_output, [])
    async def check_accuracy(self,predictions,top_n,truth):
        print('Checking accuracy')
        count = 0
        for i,prediction in predictions:
            for j in range(0,top_n):
                if(prediction[j]==truth[i]):
                    count += 1
        return float(count)/float(len(predictions))