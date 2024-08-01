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
tc = []
tipo =[]
ssd=[]


output = []
ejey = []
ejex = []
ejey1 = []
ejex1 = []
titulos = []
prof_medida=""
ssd=[]
tamCampo=""

n=0
curva_text = "none"
scan = "empty"
tc= []
df2 = pd.DataFrame()

#%DATE 30-00-24
#%DETY CHA
#%BMTY PHO
#%TYPE OPP
#%AXIS X
#%PNTS 115
#%STEP 010
#%SSD  1000
#%FLSZ 030*030
#%DPTH 050

with open("C:/Users/diego/OneDrive/Escritorio/Universidad/python/Proyectos INCAN/X15_Perfiles.ASC",'r') as data_file:
    for line in data_file:
        data=re.split('[<+>]', line)

        if line.startswith("%DPTH"): # Lo que quiero es obtener el numero de profundidades que se consideran
            profundidades.append(data)
            #pre=line.strip().split(' ')[1]
            #prof_medida=str(pre+str(n))

        if line.startswith("%FLSZ"): # Lo que quiero es obtener el numero de profundidades que se consideran
            tc.append(data)

        if line.startswith("%SSD"): # Lo que quiero es obtener el numero de profundidades que se consideran
            ssd.append(data)

profundidades_lista = []
ssd_lista = []
tc_lista =[]

for i in profundidades:
    profundidades_lista.extend(i) # Lo que hace es aplanar una lista de listas, para asi solo obtener una lista de todos los titulos de profundidades

for i in ssd:
    ssd_lista.extend(i)

for i in tc:
    tc_lista.extend(i)


tamaño_campo = []

for i in tc_lista:
    nc = i.split()
    campo = nc[1]
    tamaño_campo.append(campo)

tamaño_corregido = []

for i in tamaño_campo:
    tcc = i.split("*")
    cor = tcc[1]
    tamaño_corregido.append(cor)


prof = []

for i in profundidades_lista:
    npp = i.split()
    p = npp[1]
    prof.append(p)




#----------------------------------------------------------------------------------------------------------#

# Necesito crear listas vacias, para despues rellenarlas con datos. Seran listas de listas
listas_rellenables = [[] for i in profundidades_lista]
ejesy = [[] for i in profundidades_lista]
ejesx = [[] for i in profundidades_lista]


#----------------------------------------------------------------------------------------------------------#


with open("C:/Users/diego/OneDrive/Escritorio/Universidad/python/Proyectos INCAN/X15_Perfiles.ASC",'r') as data_file:

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
        if end > 5:
            ejeydata = re.sub("'", "", sublista[end-2]) # Aqui hay algo muy importante, sin embargo no identifico que es, solamente puedo decir que sin este comando la longitud de las listas cuando el valor es positivo incrementa
            ejesy[i].append(ejeydata) # Almacena los datos
            ejesx[i].append(sublista[end-5])

#----------------------------------------------------------------------------------------------------------#


for i, (ejes_x, ejes_y) in enumerate(zip(ejesx, ejesy)): # Algo complejo pero zip conjunta dos arreglos en una, es decir, genera una tupla que puede ir siendo indexada, pero cada arreglo tiene su variable de elementos propia
    if len(ejes_x) == len(ejes_y):  # Cuida que la longitud de los elementos sea la misma, para poder generar un data frame
        df = pd.DataFrame({
            "x": ejes_x,
            "y": ejes_y
        })

        x = pd.to_numeric(df['x'])
        y = pd.to_numeric(df['y'])

        f = interpolate.interp1d(x,y)
        maximoX= pd.to_numeric(df['x'].max())

        xMedidoInterpolado = np.arange(-maximoX,maximoX,1)
        yMedidoInterpolado = f(xMedidoInterpolado)
        df3 = pd.DataFrame()

        df3.insert(0, 'Xres', xMedidoInterpolado, False)
        df3.insert(1, 'Yres', yMedidoInterpolado, False)

        filename2 =f"tamaño de campo_{tamaño_corregido[i]}x{tamaño_corregido[i]}_profundidad_{prof[i]}.csv"
        #filename = f"lista_{i+1}_data.csv"
        df3.to_csv(filename2, index=False)
        #df.to_csv(filename, index=False)
    else:
        print(f"Error: Longitudes desiguales en lista {i+1}")

#----------------------------------------------------------------------------------------------------------#
