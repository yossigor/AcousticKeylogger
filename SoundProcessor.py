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
    async def band_pass_train_folder(self,training_folder,output_folder,center,width):
        for filename in os.listdir(training_folder):
            if filename.endswith(".wav"): 
                print("sound processor found {}".format(filename))
                output_path = os.path.join(output_folder,filename)
                print("writing to {}".format(output_path))
                await self.band_pass_file(os.path.join(training_folder,filename),output_path,center,width)
            elif filename.endswith(".txt"):
                output_path = os.path.join(output_folder,filename)
                copyfile(os.path.join(training_folder,filename),output_path)
    async def band_pass_file(self,input_file_name,output_file_name,center, width):
        print("bandpassing {}, center = {}, width = {}".format(input_file_name,center,width))
        # We run the sox application for sound processing 
        subprocess.run(["sox",input_file_name,output_file_name, "band",str(center),str(width)])
    async def band_reject_file(self,input_file_name,output_file_name,center, width):
        print("bandpassing {}, center = {}, width = {}".format(input_file_name,center,width))
        # We run the sox application for sound processing 
        subprocess.run(["sox",input_file_name,output_file_name, "bandreject",str(center),str(width)])
    async def band_reject_train_folder(self,training_folder,output_folder,center,width):
        for filename in os.listdir(training_folder):
            if filename.endswith(".wav"): 
                print("sound processor found {}".format(filename))
                output_path = os.path.join(output_folder,filename)
                print("writing to {}".format(output_path))
                await self.band_reject_file(os.path.join(training_folder,filename),output_path,center,width)
            elif filename.endswith(".txt"):
                output_path = os.path.join(output_folder,filename)
                copyfile(os.path.join(training_folder,filename),output_path)
    async def compand_file(self,input_file_name,output_file_name):
        # We run the sox application for sound processing 
        subprocess.run(["sox",input_file_name,output_file_name, "compand","0.1,0.3" ,"-90,-90,-70,-58,-55,-43,-31,-31,-21,-21,0,-20"
        ,"0", "0", "0.1"])
    async def compand_folder(self,training_folder,output_folder):
        for filename in os.listdir(training_folder):
            if filename.endswith(".wav"): 
                print("sound processor found {}".format(filename))
                output_path = os.path.join(output_folder,filename)
                print("writing to {}".format(output_path))
                await self.compand_file(os.path.join(training_folder,filename),output_path)
            elif filename.endswith(".txt"):
                output_path = os.path.join(output_folder,filename)
                copyfile(os.path.join(training_folder,filename),output_path)