import asyncio
from concurrent.futures import ProcessPoolExecutor
import os
import pprint
import itertools
import numpy as np
import importlib
from sklearn.externals import joblib
from sklearn.feature_selection import RFECV
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from Listener import Listener
from Dispatcher import Dispatcher
from Classifier import Classifier

import python_speech_features as sf
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class BaseMiner(BaseEstimator, ClassifierMixin):
    def fit(self, X, y):
        return self


class MFCC(BaseMiner):
    @staticmethod
    def transform(X):
        return np.array([sf.mfcc(sample, 44100, 0.01, 0.0025, 32, 32, preemph=0, highfreq=12000, ceplifter=0,
                       appendEnergy=False).flatten() for sample in X])

class ModelGenerator:
    def __init__(self,config):
        self.config = config
        self.files_to_mine = {}
        self.mined_files = {}
        self.wav_files = []
        self.label_files = []
        self.press_files = []
        self.wavfiles_map = {}
        self.pressfiles_map = {}
        self.f_X = []
        self.f_y = []
        self.clf = None
    def add_file(self,fl):
        ext = os.path.splitext(fl)[1]
        if ext == '.wav':
            self.wav_files.append(fl)
        elif ext == '.press':
            self.press_files.append(fl)
        elif ext == '.txt':
            self.label_files.append(fl)
    async def collect_training_files(self,training_folder_path):
        print("Collecting training files")
        print("checking {}".format(training_folder_path))
        f = os.path.abspath(training_folder_path)
        if os.path.isfile(f):
            add_file(f)
        elif os.path.isdir(f):
            for r, d, fs in os.walk(f):
                for fn in fs:
                    f1 = os.path.abspath(os.path.join(r, fn))
                    self.add_file(f1)
    async def generate_model(self,training_folder_path,model_output_path):
        pp = pprint.PrettyPrinter(indent=4)
        await self.collect_training_files(training_folder_path)
        #print("Files to mine ({}): {}".format(len(self.files_to_mine),self.files_to_mine))
        #print("Mined files ({}): {}".format(len(self.mined_files),self.mined_files))
        print("Wav files ({}):".format(len(self.wav_files)))
        pp.pprint(self.wav_files)
        print("Label files ({}):".format(len(self.label_files)))
        pp.pprint(self.label_files)
        print("Press files ({}):".format(len(self.press_files)))
        pp.pprint(self.press_files)
        await self.check_files()
        await self.process_files()
        # Load pipeline steps
        # 1 - Feature extraction
        pipeline = []
        pipeline.append(('MFCC', MFCC()))
        pipeline.append(('Scaler', MinMaxScaler()))
        # 2 - Feature selector and classifier
        classifier = getattr(importlib.import_module('sklearn.linear_model'),
         'LogisticRegression')(solver='lbfgs',multi_class='auto',max_iter=300,n_jobs=4)
        pipeline.append(('Feature Selection',
                        RFECV(classifier, step=self.f_X.shape[1] / 10, cv=5, verbose=0)))
        pipeline.append(('Classifier', classifier))
        clf = Pipeline(pipeline)
        
        print("Learning...")
        # Fit and save fitted model to file. Output stats about estimated accuracy
        clf.fit(self.f_X, self.f_y)
        print("Learning task completed!")
        #print("Writing model to disk")
        self.clf = clf
        return clf
    async def check_files(self):
        # Every wavfile and pressfile needs a corresponding label file (same name, any extension)
        # Otherwise raise an error
        print("Checking files...")
        for f in self.wav_files:
            basename = os.path.splitext(os.path.basename(f))[0]
            if os.path.splitext(f)[0] + '.press' not in self.press_files:
                self.wavfiles_map[f] = None
                for l_f in self.label_files:
                    if os.path.splitext(os.path.basename(l_f))[0] == basename:
                        self.wavfiles_map[f] = l_f
        for f in self.press_files:
            basename = os.path.splitext(os.path.basename(f))[0]
            self.pressfiles_map[f] = None
            for l_f in self.label_files:
                if os.path.splitext(os.path.basename(l_f))[0] == basename:
                    self.pressfiles_map[f] = l_f

        mismatches = [x for x, y in self.wavfiles_map.items() if y is None] + \
                    [x for x, y in self.pressfiles_map.items() if y is None]
        if len(mismatches) != 0:
            error_message = "Can't find labels for some wav files / press files!"
            offending_files = mismatches
            raise(Exception(error_message + "\n Offending files:" + str(offending_files)))
    async def process_files(self):
        print("Found {} files already mined".format(len(self.press_files)))
        print("Found {} files to mine".format(len(self.wav_files) - len(self.press_files)))
        #listening task
        listening_tasks = [];
        executor = ProcessPoolExecutor(max_workers=10)
        for i,(wav_file,label_file) in enumerate(self.wavfiles_map.items()):
            listening_tasks.append(asyncio.get_running_loop().run_in_executor(
                executor,Listener.read_wav_file,wav_file))
        wav_data_list = await asyncio.gather(*listening_tasks);
        dispatching_tasks = [];
        for wav_data in wav_data_list:
            dispatching_tasks.append(asyncio.get_running_loop().run_in_executor(
                executor,Dispatcher.offline,wav_data,self.config))
        dispatcher_output = await asyncio.gather(*dispatching_tasks);
        for i,(wav_file,label_file) in enumerate(self.wavfiles_map.items()):
            ground_truth = np.loadtxt(label_file, dtype=str)
            if len(dispatcher_output[i]) != len(ground_truth):
                # More mined events than ground truth values
                print(
                """more mined events than ground truth values. \nKeystrokes in ground truth: {}\
                    \nKeystrokes found in {}: {}
                """.format(len(ground_truth),wav_file,len(dispatcher_output[i])))
                continue
            else:
                _x = []
                # Collect results until the number of letters we know is in the file
                while len(_x) < len(ground_truth):
                    _x.append(dispatcher_output[i].pop(0))
                X = [[] for _ in range(len(_x))]
                for idx, sample in _x:
                    X[idx] = sample
                np.savetxt(os.path.splitext(wav_file)[0] + '.press', X)
                self.f_X.extend(X)
                self.f_y.extend(ground_truth)
        # .press files already present only need to be loaded from disk and appended to the matrix
        for i, (press_file, label_file) in enumerate(self.pressfiles_map.items()):
            self.f_X.extend(np.loadtxt(press_file))
            self.f_y.extend(np.loadtxt(label_file, dtype=str))
        self.f_X, self.f_y = np.array(self.f_X), np.array(self.f_y)
    async def estimateAccuracy(self):
        print("Estimating accuracy...")
        print(np.mean(cross_val_score(self.clf, self.f_X, self.f_y, cv=6)))



