
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


with open("C:/Users/diego/OneDrive/Escritorio/Universidad/python/Proyectos INCAN/X15_Perfiles.ASC",'r') as data_file:
    for line in data_file:
        data=re.split('[<+>]', line)

        if line.startswith("%DPTH"):
            profundidades.append(data)

profundidades_lista = []

for i in profundidades:
    profundidades_lista.extend(i)


listas_rellenables = [[] for i in profundidades_lista]
ejesy = [[] for i in profundidades_lista]
ejesx = [[] for i in profundidades_lista]



with open("C:/Users/diego/OneDrive/Escritorio/Universidad/python/Proyectos INCAN/X15_Perfiles.ASC",'r') as data_file:
    
    n = 0

    for line in data_file:
        data=re.split('[<+>]', line)

        if line.startswith("<"):
            inside_tag = True
            if n < len(listas_rellenables):
                listas_rellenables[n].extend([data])  # Asegúrate de que n esté dentro del rango
        elif line.startswith("$ENOM"):
            inside_tag = False
            n += 1



for i, lista in enumerate(listas_rellenables):
    for sublista in lista:
        if len(sublista) >= 4:
            ejesx[i].append(sublista[1])
            ejesy[i].append(sublista[4])




for i, (ejes_x, ejes_y) in enumerate(zip(ejesx,ejesy)):
    df = pd.DataFrame({
        "x": ejes_x,
        "y": ejes_y
    })
    filename = f"lista_{i+1}_data.csv"
    df.to_csv(filename,index=False)