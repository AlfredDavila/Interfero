"""
Author: Alfredo Dávila
Script que genera los archivos de source y axi.hist de entrada para el Axitra
poniendo fuentes de forma aleatoria
febrero 2020
Interferometría de ruido símsico

"""
from mpl_toolkits.mplot3d import Axes3D  

import matplotlib.pyplot as plt
import numpy as np

source_file = open("source", "w")
hist_file = open("axi.hist", "w")



duracion = 512 - 10
x = 42426.406871193 * 3
y = 42426.406871193 * 3
z = 30000.00
depth_min = 6000.00
n_sources = 2048
cadena = ''

x_s = []
y_s = []
z_s = []



fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

for i in range(0, n_sources):

	x_i = (np.random.rand() - 0.5) * x;
	y_i = (np.random.rand() - 0.5) * y;
	z_i = (np.random.rand() * z) + depth_min;

	x_s.append(x_i)
	y_s.append(y_i)
	z_s.append(z_i)
	ax.scatter(x_i, y_i, z_i, marker='o')

	n = (i+1)

	cadena = '{0}    {1}    {2}    {3} \n'.format(n ,x_i,y_i,z_i)

	source_file.write(cadena)

	offset_time = np.random.rand() * duracion

	vx = np.random.rand() * 2 - 1

	vy = np.random.rand() * 2 - 1

	vz = np.random.rand() * 2 - 1

	norma = (vx**2 + vy**2 + vz**2 )**(1/2)

	vx = vx / norma

	vy = vy / norma

	vz = vz / norma

	cadena_hist = '{0} {1} {2} {3} {4}e15 {5} \n'.format(n, vx, vy, vz, np.random.rand(), offset_time)
	
	hist_file.write(cadena_hist)



#Estaciones
x_estacion = 30000
ax.scatter(x_estacion, 0, 0, marker='^')
ax.scatter(-x_estacion, 0, 0, marker='^')


ax.set_xlim(-x * 1.1 /2, x* 1.1 /2)
ax.set_ylim(-y * 1.1 /2, y* 1.1 /2)
ax.set_zlim(max(z_s) * 1.1, -max(z_s) * 0.1)

ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')

plt.show()

source_file.close()
hist_file.close()









