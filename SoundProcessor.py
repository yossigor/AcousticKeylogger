import asyncio
import sys
import librosa
import os
import subprocess
from shutil import copyfile


class SoundProcessor:
    def __init__(self):
        pass
    async def time_stretch_file(self,input_file_name,output_file_name,factor):
        print("time stretching {} with factor:{}".format(input_file_name,factor))
        # We run the sox application for sound processing 
        subprocess.run(["sox",input_file_name,output_file_name, "speed",str(factor)])
    async def time_stretch_train_folder(self,training_folder,output_folder,factor):
        for filename in os.listdir(training_folder):
            if filename.endswith(".wav"): 
                print("sound processor found {}".format(filename))
                output_path = os.path.join(output_folder,filename)
                print("writing to {}".format(output_path))
                await self.time_stretch_file(os.path.join(training_folder,filename),output_path,factor)
            elif filename.endswith(".txt"):
                output_path = os.path.join(output_folder,filename)
                copyfile(os.path.join(training_folder,filename),output_path)
                