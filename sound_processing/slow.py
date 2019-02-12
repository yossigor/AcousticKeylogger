"""
Beat tracking example
"""

from __future__ import print_function
import sys
import librosa

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('supply input file path')

    #    Get the file path from the command line arguments
    FILENAME = sys.argv[1]

    #    Load the audio as a waveform `y`
    #    Store the sampling rate as `sr`
    Y, SR = librosa.load(FILENAME)

    #    Slowing down the sample
    Y_SLOW = librosa.effects.time_stretch(Y,0.5)

    #    Output the file
    librosa.output.write_wav('output.wav',Y_SLOW,SR)