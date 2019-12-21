import os
os.chdir('./')
from pydub import AudioSegment
import wave
import matplotlib
from matplotlib import pylab
import matplotlib.pyplot as plt
import numpy as np

def waveread(filename):
    song = AudioSegment.from_mp3(filename)
    song.export(filename[:-4] + '.wav', format='wav')
    wavefile = wave.open(filename[:-4] + '.wav', 'rb')
    params = wavefile.getparams()
    nchannels, sampwidth, framesrate, nframes = params[:4]
    wavedata = wavefile.readframes(nframes)
    wavefile.close()
    data = np.fromstring(wavedata, dtype=np.short)
    if nchannels == 2:
        data.shape = (-1, 2)
    data = data.T
    time = np.arange(0, nframes) * (1.0 / framesrate)
    return data, time, framesrate

def fft(filename):
    wavedata, wavetime, framesrate = waveread(filename)
    length = len(wavedata[0])
    windowsize = 5000
    time = [n for n in range(windowsize)]
    plt.figure(figsize=(20, 10), dpi=80)
    
    
    plt.ion()
    for i in range(0, length, int(windowsize / 10)):
        plt.cla()
        plt.subplot(1, 2, 1)
        plt.cla()
        inf = min(i + windowsize, length)
        c = np.fft.rfft(wavedata[0][i:inf]) / (inf - i)
        freqs = np.linspace(0, framesrate / 2, (inf - i) / 2)
        plt.grid(True)
        plt.xlabel('Freqrence/Hz')
        plt.xlim(0, framesrate / 2)
        plt.ylabel('Amp')
        plt.ylim(0, 3000)
        plt.plot(freqs, np.abs(c[:-1]))
        plt.fill_between(freqs, 0, np.abs(c[:-1]))
        plt.subplot(1, 2, 2)
        plt.grid(True)
        plt.xlabel('Time')
        plt.ylabel('Amp')
        plt.ylim(-30000, 30000)
        plt.plot(time, wavedata[0][i:inf])
        plt.pause(0.001)
    plt.ioff()
    plt.show()
        

if __name__ == '__main__':
    fft('clip.mp3')