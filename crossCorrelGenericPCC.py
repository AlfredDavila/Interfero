################################
# Script que hace la cross correlacón entre horas
# @author Alfredo Davila
# Abril 2020
#############################

import glob

import numpy as np

from pcc2_method import pcc2

from obspy import read, Trace, Stream, UTCDateTime
from obspy.core.util import AttribDict
from pathlib import Path
import matplotlib.pyplot as plt
from obspy.signal.cross_correlation import xcorr_pick_correction

from funciones import *

corr = [] 

SIZE_WINDOW = 30 * 60#segundos

COUNTS_LIMIT = 9999999

OVERLAP = 0.0


#Banderas para ejecutar el proceso


title = 'SEÑALES PCC, VENTANA {0} min'

title = title.format(SIZE_WINDOW / 60)

n_trazas = 0


folder = './MASE/'

file_name_a = '20060306000000.TO.TONI.BHZ.sac' 


file_name_b = '20060306000000.TO.TONI.BHZ.sac'


file_a = Path(folder + file_name_a)

file_b = Path(folder + file_name_b)

#si no existe alguno de los archivos envia un error
if not file_a.is_file() or not file_b.is_file():
	print('No existe alguno de los archivos', file_a.is_file(), file_b.is_file())
	exit()

else:
	print('Procesando ', file_name_b)
#Leer las trazas
st_original = read(folder + file_name_a)

st_original += read(folder + file_name_b)


#Ciclo de secciones de tiempo

start_a = st_original[0].stats.starttime

start_b = st_original[1].stats.starttime

print('Tiempos de inicio de las trazas',start_a, start_b )

if start_a != start_b:
	print('Las trazas no inician en el mismo tiempo')
	exit()

end_a = st_original[0].stats.endtime

end_b = st_original[1].stats.endtime

print('Tiempos de inicio de las trazas',end_a, end_b )

if end_a != end_b:
	print('Las trazas no finalizan en el mismo tiempo')
	exit()



n_windows = int((end_a - start_a) / (SIZE_WINDOW * ( 1 - OVERLAP))) - 1

n_windows = int(n_windows / 2.0)

print('Ventanas->', n_windows)

# taper the edges
st_original.taper(max_percentage=0.05, type='cosine')


print('Delta Origin', st_original[0].stats.delta)



for i in range(n_windows):

	print('N W', i + 1)

	st = st_original.copy()
	
	  

	#st.plot() 

	t_ini = start_a + i * SIZE_WINDOW * (1 - OVERLAP)

	#Cortar la traza
	st.trim(t_ini, t_ini + SIZE_WINDOW)

	if len(st[1].data) != len(st[0].data):
		print('Numero de muestras no coincide')
		continue


	#Eliminar la media
	st.detrend("constant")
	#Eliminar la tendencia
	st.detrend("linear")

	#Eliminar la media
	st.detrend("constant")
	

	#Decimar
	#st = decimarZeroPhase(st, 5)


	xcorr = []
	t, xcorr = pcc2(st[0].data, st[1].data, st[0].stats.delta, -SIZE_WINDOW , SIZE_WINDOW)

	#print(len(t), t[0], t[-1], len(st[1].data))

	#Normalizar 	
	xcorr_normal = xcorr #/ float((np.abs(xcorr).max()))


	#Apilar

	# Construir un arreglo con todas las correlaciones
	if len(corr) > 0:
		corr = np.vstack((corr, xcorr_normal))
	else:
		corr = xcorr_normal

	#COntador de trazas

	n_trazas = n_trazas + 1


#Apilado
stack = np.sum(corr, 0)
#Normalizado
stack = stack / float((np.abs(stack).max()))  

dt = st[0].stats.delta

print('Delta', dt)

print('Stack', len(stack))

N = len(stack)

traza_stack = Trace(data=stack)

st_resultado =  Stream(traces=[traza_stack])

#div &1,depmax


img_name = ' PCC'

print('Trazas usadas', n_trazas)


name_img_c = 'TONI_TONI_{0}_sw_{1}'.format(n_trazas, int(SIZE_WINDOW/60) ) + img_name

plotCross(stack, dt, title, img_name = name_img_c + '.png', xlim = SIZE_WINDOW)

#Poner los datos de la fuente de la otra estación

st_resultado[0].stats.sac = st_original[0].stats.sac

st_resultado[0].stats.delta = dt

st_resultado[0].stats.channel = 'CROSS'

st_resultado[0].stats.station = 'CROSS'

st_resultado[0].stats.starttime = st_original[0].stats.starttime

st_resultado[0].stats.sac['stlo'] = st_original[0].stats.sac['stlo']

st_resultado[0].stats.sac['stla'] = st_original[0].stats.sac['stla']

st_resultado[0].stats.sac['evla'] = st_original[1].stats.sac['stla']

st_resultado[0].stats.sac['evlo'] = st_original[1].stats.sac['stlo']

st_resultado[0].stats.sac['o'] = (st_resultado[0].stats.endtime - st_resultado[0].stats.starttime) / 2.0

st_resultado[0].stats.sac['ko'] = st_resultado[0].stats.starttime + (st_resultado[0].stats.endtime - st_resultado[0].stats.starttime) / 2.0

st_resultado[0].write("./{0}.sac".format(name_img_c) , format="SAC") 


#print(no_validos)
