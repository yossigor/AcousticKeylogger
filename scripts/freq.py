from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import math
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt


print('Loading audio file...')
[Fs, x] = audioBasicIO.readAudioFile("../sounds/pp.wav")
x = x[int(1*Fs):int(len(x)-1*Fs)]
#plt.plot(x)
#plt.show()
winSize = 100
winNum = int(len(x)/winSize)
sums = []
lowFilter=3
highFilter=20
for i in range(0,winNum-1):
    currentWindow = fft.fft(x[i:i+winSize])
    sums.append(0);
    for j in range(1+lowFilter,int(len(currentWindow)/2)-1-highFilter):
        print(j)
        sums[i] += abs(currentWindow[j])
plt.plot(sums)
plt.show()
