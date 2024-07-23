
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



with open("C:/Users/diego/OneDrive/Escritorio/Universidad/python/Proyectos INCAN/X15_Perfiles.ASC",'r') as data_file:
    
    n = 0

    for line in data_file:
        data=re.split('[<+>]', line)

        if line.startswith("<"):
            inside_tag = True
            if n < len(listas_rellenables):
                listas_rellenables[n].extend(data)  # Asegúrate de que n esté dentro del rango
        elif line.startswith("$ENOM"):
            inside_tag = False
            n += 1



for i, lista in enumerate(listas_rellenables):
    df = pd.DataFrame(lista, columns=['Datos'])
    filename = f'archivo_{i + 1}.csv'
    df.to_csv(filename, index=False)
    print(f'DataFrame guardado en {filename}')