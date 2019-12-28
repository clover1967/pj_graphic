import os
os.chdir('./')
import sys
from pydub import AudioSegment
import wave
import matplotlib
from matplotlib import pylab
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

speed = 2               #窗口移动速度，窗口内的点全部出现到全部消失经过speed帧
windowsize = 8000       #每帧显示的采样点个数

def waveread(filename):                     #读入mp3文件并将其转化成wav文件
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

def onPress(event):
    sys.exit(0)

def fft(filename):                          #对输入的wav文件取窗口长度的点作傅立叶变换并绘制时域频域图
    wavedata, wavetime, framesrate = waveread(filename)
    length = len(wavedata[0])
    time = [n for n in range(windowsize)]
    
    plt.figure(figsize=(20, 10), dpi=80)
    plt.ion()

    for i in range(0, length, int(windowsize / speed)):
        #刷新图像
        plt.cla()

        #左声道频域
        plt.subplot(2, 2, 1)
        plt.cla()
        inf = min(i + windowsize, length)
        lf = np.fft.rfft(wavedata[0][i:inf]) / (inf - i)
        freqs = np.linspace(0, framesrate / 2, (inf - i) / 2)
        plt.grid(True)
        plt.xlabel('Freqrence/Hz')
        plt.xlim(0, framesrate / 2)
        plt.ylabel('Amp')
        plt.ylim(0, 200)
        plt.plot(freqs, np.abs(lf[:-1]), color='r')
        plt.fill_between(freqs, 0, np.abs(lf[:-1]), color='r')

        #左声道时域
        plt.subplot(2, 2, 2)
        plt.cla()
        plt.grid(True)
        plt.xlabel('Time')
        plt.ylabel('Amp')
        plt.ylim(-30000, 30000)
        plt.plot(time, wavedata[0][i:inf], color='y')

        #右声道频域
        plt.subplot(2, 2, 3)
        plt.cla()
        rf = np.fft.rfft(wavedata[1][i:inf]) / (inf - i)
        plt.grid(True)
        plt.xlabel('Freqrence/Hz')
        plt.xlim(0, framesrate / 2)
        plt.ylabel('Amp')
        plt.ylim(0, 200)
        plt.plot(freqs, np.abs(rf[:-1]), color='b')
        plt.fill_between(freqs, 0, np.abs(rf[:-1]), color='b')

        #右声道时域
        plt.subplot(2, 2, 4)
        plt.cla()
        plt.grid(True)
        plt.xlabel('Time')
        plt.ylabel('Amp')
        plt.ylim(-30000, 30000)
        plt.plot(time, wavedata[1][i:inf], color='g')

        #定义退出按钮
        button = Button(plt.axes([0., 0., 0.1, 0.1]), 'exit')
        button.on_clicked(onPress)

        #刷新间隔时间
        plt.pause(0.0001)

    plt.ioff()
    plt.show()
        
if __name__ == '__main__':
    fft(sys.argv[1])