import re
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
import pandas as pd
from prettytable import PrettyTable
import modulo_funciones as mf


def error_rel(x,y):
     diferencias = []
     espesor= len(x)
     t = 0

     for i in range(espesor):
          dif = abs(((x[i] - y[i])/(x[i]))*100)
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
          dif = abs(((x[i] - y[i])/(x[i]))*100)
          diferencias.append(dif)
          
     return diferencias
              


arch = open("C:/Users/diego/Downloads/PDD310.csv")
n = -1

depth = []

acceso = False

for line in arch:
    line = line.strip()
    nom = line.split(",")
    if line.startswith("Depth"): # Lo que quiero es obtener el numero de tamaños de campo que se consideran
            nom2 = nom[0]
            nom2 = nom2.rsplit(" ")
            nom3 = nom2[8] + "]"
            nom4 = nom2[12]
            nom5 = nom3 + nom4
            depth.append(nom5)


listas_rellenables = [[] for i in depth]
ejesy = [[] for i in depth]
ejesx = [[] for i in depth]


arch.seek(0)


for line in arch:
    line = line.strip()
    nom = line.split(",")

    if line[0] == "0":
         n +=1

    if line[0].isdigit(): 
        acceso = True

        listas_rellenables[n].append(nom)  # Va a generar una lista con indice n, donde metere listas de valores, hasta que se lea ENOM, una vez que lo haya leido, lo que hara es sumar un 1 a esa n, por lo que creara una n = 2.

        

arch.close() 



for i, lista in enumerate(listas_rellenables): # El i indice el indice y lista los elementos dentro de listas rellenables, es decir, puedo estar en la lista 1, compuesta de varias listas
    for sublista in lista: # Sublista es un elemento de la variable lista
        end = len(sublista) # Determinamos el tamaño de esta sublista
        
        ejeydata = re.sub("'", "", sublista[end-1]) # Aqui hay algo muy importante, sin embargo no identifico que es, solamente puedo decir que sin este comando la longitud de las listas cuando el valor es positivo incrementa
        ejeydata = float(ejeydata)
        ejesy[i].append(ejeydata) # Almacena los datos
        ejexdata = sublista[end-2]
        ejexdata = float(ejexdata)
        ejesx[i].append(ejexdata)


# Proceso de normalización

ejey_norm = [[] for i in depth]

for i, lista in enumerate(ejesy):
     for sublista in lista:
          maximo = max(lista)
          val_y = (sublista/maximo) * 100
          ejey_norm[i].append(val_y)

# Una vez que normalizamos, debemos interpolar, empecemos por el campo de 3 por 3

tamx = int(max(ejesx[0]))
tope = tamx + 1

x = np.linspace(0,tamx,tope)
interp1 = mf.interpolacionPDD(ejesx[0],ejey_norm[0])



#--------------------------------------------------------------------

tamañox = len(ejesx)
tamañoy = len(ejesy) 


print("----------------------------------------------------")
print(f"El archivo .csv tuvo {tamañox} PDD:")

for i in range(tamañox):
    print(depth[i])

print("----------------------------------------------------")
## Ahora vamos a subir los archivos que queremos comparar:

## Una vez que sabemos los campos, es más facil 

df = pd.read_csv("C:/Users/diego/OneDrive/Escritorio/Universidad/Github/Codigos-universidad/tamaño de campo_030x030.csv")

# Obtener listas de las dos columnas
ejex = df.iloc[:, 0].tolist()  # Primera columna
ejey = df.iloc[:, 1].tolist()  # Segunda columna



print("----------------------------------------------------")

print(f"{error_rel(ejey, interp1)}")

print("----------------------------------------------------")
print()
print()


error_relativo = error_vector(ejey, interp1)


#---------------------------------------------------------------------------------------------

#for i, (x, ejey,interp1) in enumerate(zip(x, ejey,interp1)):


#---------------------------------------------------------------------------------------------
# Grafico de la comparación de PDD

plt.figure()
plt.plot(ejex, ejey, "b--", label = "Valores obtenidos en archivo ASC")
plt.plot(x,interp1, "--r", label = "Valores obtenidos en archivo CSV")
plt.plot(ejex, error_relativo, "xg", label = "Error relativo")
plt.title("Comparación entre valores obtenidos por archivo CSV y por archivos ASC, PDD")
plt.xlabel("Profundidad [mm]")
plt.ylabel("Porcentaje de Dosis")
plt.legend()
plt.grid()
plt.show()