import asyncio
import os
import pprint

class ModelGenerator:
    def __init__(self):
        self.files_to_mine = {}
        self.mined_files = {}
        self.wav_files = []
        self.label_files = []
        self.press_files = []
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
    async def check_files(self):
        # Every wavfile and pressfile needs a corresponding label file (same name, any extension)
        # Otherwise raise an error
        print("Checking files")
        wavfiles_map = {}
        for f in self.wav_files:
            basename = os.path.splitext(os.path.basename(f))[0]
            if os.path.splitext(f)[0] + '.press' not in self.press_files:
                wavfiles_map[f] = None
                for l_f in self.label_files:
                    if os.path.splitext(os.path.basename(l_f))[0] == basename:
                        wavfiles_map[f] = l_f
        pressfiles_map = {}
        for f in self.press_files:
            basename = os.path.splitext(os.path.basename(f))[0]
            pressfiles_map[f] = None
            for l_f in self.label_files:
                if os.path.splitext(os.path.basename(l_f))[0] == basename:
                    pressfiles_map[f] = l_f

        mismatches = [x for x, y in wavfiles_map.items() if y is None] + \
                    [x for x, y in pressfiles_map.items() if y is None]
        if len(mismatches) != 0:
            error_message = "Can't find labels for some wav files / press files!"
            offending_files = mismatches
            raise(Exception(error_message + "\n Offending files:" + str(offending_files)))