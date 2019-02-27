# Acoustic Keylogger
A python based software implementing keyboard acoustic eavesdropping attacks by training a machine learning classifier using only the acoustic fingerprints of a user keystrokes.

## Table of Contents
- [Introduction](#introduction)
- [Previous projects](#previous-projects)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Training a model](#training-a-model)
- [The attacks](#the-attacks)
    * [Classification attack](#classification-attack)
    * [Smart Dictionary attack](#smart-dictionary-attack)
- [Authors](#authors)
- [Advisors](#advisors)

## Introduction
The purpose of this project is to explore the viability and effectiveness of a new type of keylogger. Instead of using a malware installed on the target computer itself to record keystrokes, an acoustic keylogger can be deployed on a separate dedicated device and monitor keystrokes on another keyboard based on the acoustic sound fingerprinting.

## Previous projects
[Skype&Type project ](https://github.com/SPRITZ-Research-Group/Skype-Type) had already implemented an acoustic keylogging program. You can see the project as presented by Daniele Lain in Black Hat USA 2017 [video](https://www.youtube.com/watch?v=iD9Obu7NWso).
The details of the implemetation can be found in this [paper](https://arxiv.org/abs/1609.09359).
our project is based on S&T with a few upgrades and new features.

## Project structure
- The folder Skype-Type @ 0c0c88b contains S&T project. We converted it to python 3 and used asynchronous library instead of multi-process scripts.
- The main bulding blocks:
    * ModelGenerator.py - trains a model.
    * Dispatcher.py - extracts keypress sounds from the .wav file.
    * Listener.py - responsible for loading sound files.
    * SoundProcessor.py - responsible for the preprocessing of a .wav file.
- write_model_to_disk.py - the script fot training a model.
- The attacks:
    * classification_attack.py
    * get_smart_dictionary.py

## Requirements
In order to use our software you must have the following requirements:
- Python 3.x 
- pip - python package manager
- numpy
- sklearn
- python_speech_features

## Training a model
In order to train a model you should prepare a folder containing pairs of .wav files and .txt files (the "ground truth").
Use this command to generate the model:
> python3.7 write_model_to_disk.py --training_folder <trainig folder path> --output <model output path>

for more information check our [wiki](https://github.com/yossigor/AcousticKeylogger/wiki).

## The attacks

### Classification attack
After generating a model, the classification attack is used to classify the keystrokes from a .wav file. For example, if you have a model that was trained for the victim's keyboard and you have another file with unknown keystrokes you can use the Acoustic keylogger to classify those keystrokes.
Use this command to perform the attack:
> python3.7 classification_attack.py --target_file <target file> --model_file <model file>

for more information check our [wiki](https://github.com/yossigor/AcousticKeylogger/wiki).

### Smart Dictionary attack
This attack is used to generate a dictionary for the victim's password. You will need a trained model and a folder containing recordings of the victim's password.
Use this command to perform the attack:
> python3.7 get_smart_dictionary.py --passwords_recordings_folder <passwords folder> --dictionary_output <dictinary output file> --model_file <model file>

for more information check our [wiki](https://github.com/yossigor/AcousticKeylogger/wiki).

## Authors
[Meshi Fried](https://github.com/MeshiFried) and [Yossi Gorshomov](https://github.com/yossigor)
Technion - Israel Institute of Technology

## Advisors
Danny Tylman Amir Schwartz

