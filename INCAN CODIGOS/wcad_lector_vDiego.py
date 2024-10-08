# Instituto nacional de cancerologia
# Hecho por Diego Medel
# 23/07/24


import re
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
import pandas as pd

#import matplotlib.pyplot as plt

inside_tag = False
profundidades = []
output = []
ejey = []
ejex = []
ejey1 = []
ejex1 = []
titulos = []
n=0
curva_text = "none"
scan = "empty"
tc= "none"
df2 = pd.DataFrame()


with open("C:/Users/diego/OneDrive/Escritorio/Universidad/INCAN/Archivos ASC/X06 FFF Perfiles smooth 1mm.ASC",'r') as data_file:
    for line in data_file:
        data=re.split('[<+>]', line)

        if line.startswith("%DPTH"): # Lo que quiero es obtener el numero de profundidades que se consideran
            profundidades.append(data)

profundidades_lista = []

for i in profundidades:
    profundidades_lista.extend(i) # Lo que hace es aplanar una lista de listas, para asi solo obtener una lista de todos los titulos de profundidades


#----------------------------------------------------------------------------------------------------------#

# Necesito crear listas vacias, para despues rellenarlas con datos. Seran listas de listas
listas_rellenables = [[] for i in profundidades_lista]
ejesy = [[] for i in profundidades_lista]
ejesx = [[] for i in profundidades_lista]


#----------------------------------------------------------------------------------------------------------#


with open("C:/Users/diego/OneDrive/Escritorio/Universidad/INCAN/Archivos ASC/X06 FFF Perfiles smooth 1mm.ASC",'r') as data_file:
    
    n = 0

    for line in data_file:
        data=re.split('[<+>]', line)

        if line.startswith("<"): # Si empieza con el simbolo < entonces que continue
            inside_tag = True
            if n < len(listas_rellenables): # Cuida que no se pase del rango
                listas_rellenables[n].append(data)  # Va a generar una lista con indice n, donde metere listas de valores, hasta que se lea ENOM, una vez que lo haya leido, lo que hara es sumar un 1 a esa n, por lo que creara una n = 2.

        elif line.startswith("$ENOM"):
            inside_tag = False
            n += 1

#----------------------------------------------------------------------------------------------------------#


for i, lista in enumerate(listas_rellenables): # El i indice el indice y lista los elementos dentro de listas rellenables, es decir, puedo estar en la lista 1, compuesta de varias listas
    for sublista in lista: # Sublista es un elemento de la variable lista
        end = len(sublista) # Determinamos el tamaño de esta sublista
        ejeydata = re.sub("'", "", sublista[end-2]) # Aqui hay algo muy importante, sin embargo no identifico que es, solamente puedo decir que sin este comando la longitud de las listas cuando el valor es positivo incrementa
        ejesy[i].append(ejeydata) # Almacena los datos
        ejexdata = re.sub("'","", sublista[end-5])
        ejesx[i].append(ejexdata)

#----------------------------------------------------------------------------------------------------------#


for i, (ejes_x, ejes_y) in enumerate(zip(ejesx, ejesy)): # Algo complejo pero zip conjunta dos arreglos en una, es decir, genera una tupla que puede ir siendo indexada, pero cada arreglo tiene su variable de elementos propia
    if len(ejes_x) == len(ejes_y):  # Cuida que la longitud de los elementos sea la misma, para poder generar un data frame
        df = pd.DataFrame({
            "x": ejes_x,
            "y": ejes_y
        })
        filename = f"lista_{i+1}_data.csv"
        df.to_csv(filename, index=False)
    else:
        print(f"Error: Longitudes desiguales en lista {i+1}")

#----------------------------------------------------------------------------------------------------------#
