################################
# Script que calcula la cross 
# correlación entre dos señales
# @author Alfredo Davila
# Marzo 2020
#############################

import matplotlib.pyplot as plt

import numpy as np

def cross_corr(x, y):
    
    N = len(y) if len(x) < len(y) else len(x)
    
    #Completar con zeros
    if len(x) < len(y) and len(x) != len(y):
        for i in range(N - len(x)):
            x.append(0)
    elif len(x) != len(y):
        for i in range(N - len(y)):
            y.append(0)
            
    
    
    correlacion = [0]*(2*N-1)
    
    #Formar la x para la correlacion
    x_extend = [0]*(N - 1)
    x_extend.extend(x)
    
    
    
    
    for l in range(2 * N - 1):
        #Forma la y para la correlacion cada iteracion se recorre
        y_extend = []
        
        #Zeros al inicio
        y_extend = [0]*(l)
        #Luego la señal
        y_extend.extend(y)
        #Zeros al final
        y_extend.extend([0]*(2 * N + 1 - l))
        
        y_extend = y_extend[0:N * 2 - 1]
        
        #print('l=',l)
        #print(x_extend)
        #print(y_extend)
        
        #Hacemos la convolucion
        for i in range(2 * N - 1):
            
            correlacion[l] = correlacion[l] + x_extend[i] * y_extend[i]
        
    correlacion_norm = [x / max(correlacion) for x in correlacion]
    return correlacion_norm
    
def get_puerta(tau, n_points_width, dt, t_fin):
    t = np.arange(0, t_fin, dt)
    
    y = int(tau/dt) * [0]
    
    y.extend(n_points_width * [1])
    
    y.extend( (len(t)-len(y))  * [0] )
    
    return t, y
 
def plot_correlacion(t, x, y, correlacion):
    N = len(x)

    t_all = np.arange(-max(t) - 0.0099, max(t), 0.01)
    
    fig, ax = plt.subplots(1, 1)
    
    out = ax.plot(t_all, correlacion, linestyle='--', marker='', label='Correlación')
    
    #pirata = np.correlate(x,y, 'full')
    
    out = ax.plot(t, x, linestyle='-', marker='', label='X')
    
    out = ax.plot(t, y, linestyle='-', marker='', label='Y')
    
    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Correlación')
    ax.set_xlabel('tiempo')
    ax.set_ylabel('Valor de la correlacion')
    
    plt.show()

t, x = get_puerta(tau = 5, n_points_width = 1, dt = 0.01, t_fin = 20)

t, y = get_puerta(tau = 7, n_points_width = 200, dt = 0.01, t_fin = 20)



corr = cross_corr(x, y)

#plot_correlacion(t, x, y, corr)

corr = cross_corr(y, x)

#plot_correlacion(t, x, y, corr)

t, z = get_puerta(tau = 5, n_points_width = 1, dt = 0.01, t_fin = 20)

corr = cross_corr(x, z)

#plot_correlacion(t, x, z, corr)

seno = np.sin(t)

seno[:314] = 0

seno[314 * 3:] = 0

corr = cross_corr(x, seno)

plot_correlacion(t, x, seno, corr)
