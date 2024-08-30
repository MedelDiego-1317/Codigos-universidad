import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

def interpolacionPDD(x,y):

    xmax = int(max(x))
    tope = xmax + 1
    tamaño_inter = np.linspace(0,xmax,tope)

    fun = InterpolatedUnivariateSpline(x,y,k=3)
    inter = fun(tamaño_inter)

    return inter


def error_rel(x,y):
     diferencias = []
     espesor= len(x)
     t = 0

     for i in range(espesor):
          dif = abs(((x[i] - y[i])/(y[i]))*100)
          diferencias.append(dif)
          
          if dif > 10:
               t += 1
              

     error_maximo = max(diferencias)
     error_medio = np.mean(np.array(diferencias))

     return f"El error maximo fue de {error_maximo}, el error medio fue de {error_medio} y el numero de valores que superan el 10% son {t}" 


def error_vector(x,y):
     diferencias = []
     espesor= len(x)
     t = 0

     for i in range(espesor):
          dif = abs(((x[i] - y[i])/(y[i]))*100)
          diferencias.append(dif)
          
     return diferencias

