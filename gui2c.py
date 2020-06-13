########################################################################
### 17,November,2018                                                 ###
### By : Reza Amini , University of Tabriz                           ###
########################################################################
### easy way to watch EDF files                                      ###
### multi-channel wathing with flitered and fft data simultaneously  ###
########################################################################


from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pyedflib
from scipy import signal
import scipy.fftpack



def showlabels():

    messagebox.showinfo("labels", signal_labels)

def fileinput():
    global filename
    global eegFile
    filename=  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("EDF files","*.edf"),("all files","*.*")))
    eegFile = pyedflib.EdfReader(filename)

    global signal_labels
    signal_labels = eegFile.getSignalLabels()
    global xaxis
    xaxis = []
    for i in range(19920):
        xaxis.append(i)


    totalSignals = eegFile.signals_in_file #totalSignals = 64
    global data
    data = np.zeros((totalSignals, eegFile.getNSamples()[0]-80))
    for i in np.arange(totalSignals):
        data[i, :] = eegFile.readSignal(i)[:-80]
    
def showeeg():
    global data_s
    data_s=data[which_electrode]
    plt.plot(xaxis,data_s)
    plt.xlabel('1/160 of a second')
    plt.ylabel('EEG µV(?)')
    plt.title('EEG Motor Movement/Imagery Dataset')
    plt.show()


def filteredshow():
    fs=1024
    order=5
    Fpa=1
    Fpb=80
    Wpb = Fpb/(fs/2) # Para o filtro PASSA-BAIXA
    Wpa = Fpa/(fs/2) # Para o filtro PASSA-ALTA
    fdata=data_s
    b2, a2 = signal.butter(order, Wpa, 'highpass') # Design butter filter - Fc = 10Hz
    b3, a3 = signal.butter(order, Wpb, 'lowpass') # Design butter filter - Fc = 20Hz
    passaAlta = signal.filtfilt(b2, a2, fdata) # Passa um filtro PASSA-ALTA para remover nível DC do SINAL
    passaBaixa = signal.filtfilt(b3, a3, passaAlta) # Passa um filtro PASSA-BAIXA no SINAL retificado
    plt.plot(xaxis, passaBaixa)
    plt.xlabel('1/160 of a second')
    plt.ylabel('Filtered EEG µV(?)')
    plt.title('EEG Motor Movement/Imagery Dataset  (Filtered)')
    plt.show()



def FFT():
    fs=1024
    N = len(data_s)
    t = np.array(range(N))/fs
    # sample spacing
    T = 1.0 / float(fs)
    x = np.linspace(0.0, N*T, N)
    fftda=data_s
    yf = scipy.fftpack.fft(fftda)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.show()


def gett():
    global which_electrode
    g=E1.get()
    which_electrode= signal_labels.index(g)



win = Tk()
win.title("EDF Reader")
win.geometry('300x200')



btn1 = Button(win, text="Browse File  ",command=fileinput)
btn1.grid(  column=1, row=0)


btn2 = Button(win, text="Show me electrodes",command=showlabels)
btn2.grid(column=1, row=1)


L1 = Label(win, text="Which Electrode:")
L1.grid(column=1, row=2)

v = StringVar()
E1 = Entry(win, textvariable=v)
E1.grid(column=2, row=2)
b = Button(win, text="get",  command=gett)
b.grid(column=3, row=2)




btn3 = Button(win, text="Show me data",command=showeeg)
btn3.grid(column=1, row=3)

btn4 = Button(win, text="Show me filtered data",command=filteredshow)
btn4.grid(column=1, row=4)



btn5 = Button(win, text="Show me FFT ",command=FFT)
btn5.grid(column=1, row=5)



win.mainloop()
