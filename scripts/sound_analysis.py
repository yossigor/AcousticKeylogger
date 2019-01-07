from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import math
import numpy as np
import matplotlib.pyplot as plt

print('Loading audio file...')
[Fs, x] = audioBasicIO.readAudioFile("../sounds/password.wav")
window=0.05*Fs
step=0.05*Fs
F, f_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.08*Fs,40);
plt.subplot(2,1,1); plt.plot(x); plt.xlabel('Frame no'); plt.ylabel('signal'); 
energy = F[1,:]
count_strokes = 0
energy_window = 2
energy_treshhold = 0.046
print(energy);
i=0
while int(i+energy_window)<len(F[1,:]):
    energy_sum = sum(energy[i:int(i+energy_window)])
    print(energy_sum)
    if(energy_sum>energy_treshhold):
        count_strokes+=1
    i = int(i+energy_window)
print(count_strokes)
#plt.show()
#print('Fs={}'.format(Fs))
#print('x={}'.format(x))

