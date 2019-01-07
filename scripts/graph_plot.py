import matplotlib.pyplot as plt
import random
import pyaudio
import numpy as np
import numpy.fft as fft
import wave
import struct
import sounddevice as sd
import time

fs = 44100
freq1 = 440
freq2 = 523.25
CHUNK = 1024
X = np.arange(0,10,1/fs)
Y = 0.5*np.sin(freq1*X*2*np.pi) + 0.5*np.sin(freq2*X*2*np.pi)
'''plt.plot(X,Y)
plt.show()'''
array = fft.fft(Y)
freq = fft.fftfreq(array.size,d=fs)
ind = np.arange(0,int(len(array)/2))
psd = abs(array[ind])**2+abs(array[-ind])**2
print(freq[ind])
plt.plot(freq[ind],psd)
plt.show()
'''sd.play(Y,fs)
time.sleep(10)
sd.stop()'''




'''
wf = wave.open('sounds/2018_10_16_17_12_51.wav', 'rb')
data = wf.readframes(-1)
fs = wf.getframerate()
print(fs);
array = np.fromstring(data, 'Int32')
print(len(array));
time=np.linspace(0, len(array)/fs, num=len(array))
plt.plot(time,array)
fft_array = fft.fft(array)
freq = fft.fftfreq(len(array),1/44100)
plt.plot(freq)
plt.show()
'''
'''
(X,Y) = ([],[])
for i in range(1,100):
    X.append(i)
    Y.append(random.random()) 
plt.plot(X,Y)
plt.ylabel('some numbers')
plt.show()
'''