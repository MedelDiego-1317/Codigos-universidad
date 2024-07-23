
import re
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
import pandas as pd

#import matplotlib.pyplot as plt

inside_tag = False
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

        if line.startswith("<"): 
            inside_tag = True
            output.append(data)
        elif line.startswith("$ENOM"):
             inside_tag = False

print(output)