import matplotlib.pyplot as plt

from datetime import datetime

import scipy.fftpack

import numpy as np

import sys

def getStartTime(date, time):
    
    #'date': 'DEL (GMT) 16/JUN/13', 'time': '05:19:28.00'
    #datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    

    dateList =  (date.split()[-1]).split('/')
    if int(dateList[-3]) > 1900:
        anio = dateList[-3]

        mes = dateList[-2]

        dia = dateList[-1]

        datetime_str = '{0}/{1}/{2} {3}'.format(mes, dia, anio, time)

        dateS = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M:%S.%f')
    else:
        anio = dateList[-1]

        mes = dateList[-2]

        dia = dateList[-3]

        datetime_str = '{0}/{1}/{2} {3}'.format(mes, dia, anio, time)

        dateS = datetime.strptime(datetime_str, '%b/%d/%y %H:%M:%S.%f')

    return dateS

def getLat(Line):
    line = Line.lower().strip()
    columns = line.split()

    lat = float(columns[-3])

    sig = -1 if columns[-1] == 's' else 1
    
    return lat * sig

def getLon(Line):
    line = Line.lower().strip()
    columns = line.split()
    
    lon = float(columns[-3])

    sig = -1 if columns[-1] == 'w' else +1
    
    return lon * sig

def getTime(line):
    """Obiene la fecha del registro"""
    
    line = line.strip()
    columns = line.split()
    
    return columns[-1]

def getDate(line):
    """Obiene la hora del registro"""
    line = line.strip()
    columns = line.split()
    date = columns[-5] + ' ' + columns[-3] + ' ' + columns[-1]
    return date

def getDT(line):
    """Obiene el periodo de muestreo del registro"""
    line = line.strip()
    
    columns = line.split()
    dt = columns[-1].split('/')
    
    dts = float(dt[-3])
    
    return dts

def getLabels(line):
    """Obiene las compoentes"""
    line = line.strip()
    
    columns = line.split()
    
    return columns
def getName(line):
    """Obtiene el nombre de la estacion"""
    columns = line.strip().split(':')
    return columns[1].strip()
def fftXY(y, T):
    #Espectro de Fourier
    
    N = len(y)
    
    yf = scipy.fftpack.fft(y)

    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    yn = 2.0/N * np.abs(yf[:N//2])
    
    return xf, yf, yn

def readSAS(nameFile, getData = True):
    """Lee los datos de un archivo SAS"""
    #Lat Lon de el receptor

    with open( nameFile, 'r',encoding = "ISO-8859-1" ) as f:
        #Funciones que se realizan en cada linea

        metaData = dict()

        for nRow  in range(1,110):
            line = f.readline()
            if nRow in N_ROW_TAG:

                tag = N_ROW_TAG[nRow]

                metaData[tag] = LINE_FNC[tag](line)

        metaData['timeStart'] = getStartTime(metaData['date'], metaData['time'])

        data = [[], [], []]
        if getData:
            for line in f:

                line = line.strip()
                columns = line.split()
                for j in range(len(columns)):

                    data[j].append(float(columns[j]))
            f.close() 

            N = len(data[1])

            fd = np.linspace(0.0, float(N * metaData['dt']), num = N, endpoint=False)
        else:
            N = 0
            fd = []
    
        print('Lectura completa de ' + nameFile)

    return metaData, data, fd



def plotSAS(metaData, data, fd):

        
    fig, axs = plt.subplots(3, 2, figsize=(8, 12))
    #, figsize=(8, 12), sharey=True
    
    f = []
    ampN = []

    #maxAmpl = max(max(data),key=abs)
    #limAmpl = (maxAmpl * 1.05)
    for i in range(len(data)):

        #axs[i][0].set_ylim(limAmpl, -limAmpl)

        axs[i][0].plot(fd, data[i], 'k-')
        
        axs[i][0].set_title(metaData['label'][i])
        
        f, amp, ampN = fftXY(data[i], metaData['dt'])

        axs[i][1].plot(f, ampN, 'k-')
        #axs[i, 1].magnitude_spectrum(data[i], Fs = 1 / metaData['dt'], color='C1',scale='dB')

        axs[i][1].set_xlim(0, 15)
        
        axs[i][0].set_xlim(0, len(data[i]) * metaData['dt'])

        axs[i][0].tick_params(axis='x',         
                                which='both',     
                                bottom=False,      
                                top=False,        
                                labelbottom=False)
        axs[i][1].tick_params(axis='x',         
                                    which='both',     
                                    bottom=False,      
                                    top=False,        
                                    labelbottom=False)
        axs[i][0].grid()
        axs[i][1].grid()
        
        #ax1.set_ylabel(metaData['dt'])
        

    subtitulo = metaData['name'] + "\n" + metaData['date'] + ' ' + metaData['time']
    fig.suptitle(subtitulo)
    axs[2][0].tick_params(axis='x',         
                                which='both',     
                                bottom=True,      
                                top=False,        
                                labelbottom=True)
    axs[2][1].tick_params(axis='x',         
                                which='both',     
                                bottom=True,      
                                top=False,        
                                labelbottom=True)
    axs[2][0].set_xlabel('ACELEROGRAMA')
    axs[2][1].set_xlabel('ESPECTROGRAMA')
    
    plt.show()

N_ROW_TAG = {47: 'dt',  57: 'date', 68:  'time', 108 : 'label', 16 : 'name', 23: 'lat', 24: 'lon'};

LINE_FNC = {'dt': getDT, 'date' : getDate, 'time': getTime, 'label' : getLabels, 'name': getName, 'lat' : getLat, 'lon' : getLon};

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso readSAS.py pathTo/nombreDeArchivoSAS')
    else:
        metaData, data, fd = readSAS(sys.argv[1])
        
        plotSAS(metaData, data, fd)
