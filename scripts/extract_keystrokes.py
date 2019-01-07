from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import math
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt

print('Loading audio file...')
[Fs, x] = audioBasicIO.readAudioFile("../sounds/pp.wav")
x = x[int(1*Fs):int(len(x)-1*Fs)]
winSize = 50
print('our window size is {} samples ({}/{}={} seconds)'.format(winSize,winSize,Fs,winSize/Fs));
winNum = int(len(x)/winSize);
print('we have {} windows'.format(winNum));
clickSizeInSeconds =0.08;
clickSize = int(Fs*clickSizeInSeconds);
print('we expect the click length to be {} seconds which is {} samples'.format(clickSizeInSeconds,clickSize));
sums = []
for i in range(0,winNum-1):
    print('calculating fft of {} window'.format(i))
    currentWindow = fft.fft(x[i:i+winSize])
    print('calculating the sum of fft vector')
    sums.append(0);
    print('size of fft is {}'.format(len(currentWindow)))
    for j in range(0,len(currentWindow)-1):
        print(abs(currentWindow[j]))
        sums[i] += abs(currentWindow[j])/2
    print('sums[{}]={}'.format(i,sums[i]))
print('calculating the click positions')
clickPositions = []
offsetToNextClick = int(clickSize/winSize);
print('we use offsetToNextClick={} samples'.format(offsetToNextClick))
h=0;
threshhold = 1070;
clicksTreshold = [];
print('we use threshhold={}'.format(threshhold))
while(h<len(sums)):
    if(sums[h]>threshhold):
        position = h*winSize;
        clicksTreshold.append(sums[h]);
        clickPositions.append(position)
        print('found click in position {} samples (after {} seconds) with sum={}'.format(position,position/Fs,sums[h]))
        h+=offsetToNextClick
    else:
        h+=1
print('{} clicks was found'.format(len(clickPositions)))

'''
y = np.arange(0, len(x));
ones = np.ones(len(x));
thr = threshhold * ones;
plt.plot(y, x, y, thr, 'r');
plt.show();
'''xlabel('windows (fixed intervals)')
ylabel('Sum of FFT coefficients')
'''
