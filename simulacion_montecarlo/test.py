import os
import math
import random
from datetime import datetime as dt
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


subprocess.run('clear', shell=True)

msg_seg = 'Presione un tecla para continuar: '

def report(__list_steps__):
    for i in __list_steps__:
        file_name = str(__list_steps__[i][0]).replace(': ', '')
        file_name = file_name.replace('\t- ', '') + '.csv'
        file_dir = os.path.join('src', file_name)
        __list_steps__[i][1].to_csv(file_dir, index=False)
        print(file_dir)

while True:
    num_interaciones = input('Introduzca el numero de simulaciones: ')
    if num_interaciones.isdigit():
        num_interaciones = int(num_interaciones)
        break
    else:
        print('Ingrese un número válido.')    


time_A = dt.now()

# Generamos el Dataframe de Entradas
archivo_excel = 'calculo_riesgos.xlsm'
nombre_hoja = '0'

    ## Lee los datos de la hoja de cálculo en un dataframe
activities_df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)
activities_df = activities_df[activities_df["Ruta_Critica"] == 1]
print(activities_df)

    ## Ampliamos el DataFrame
activities_df['Media_(mu)']  = (activities_df['Max'] + 4*activities_df['Probable'] + activities_df['Min']) / 6
activities_df['sigma']       = (activities_df['Max'] - activities_df['Min']) / 6
activities_df['sigma^2']     =  activities_df['sigma']**2
activities_df['alpha']       = ((activities_df['Media_(mu)'] - activities_df['Min']) / (activities_df['Max'] - activities_df['Min'])) * (((activities_df['Media_(mu)'] - activities_df['Min']) * (activities_df['Max'] - activities_df['Media_(mu)']) / activities_df['sigma']**2) - 1)
activities_df['beta']        = ((activities_df['Max'] - activities_df['Media_(mu)']) / (activities_df['Media_(mu)'] - activities_df['Min'])) * activities_df['alpha']

    ## Determinamos las sumas del DataFrame extendido
scale = [round(activities_df.iloc[:, i].sum()) for i in range(len(activities_df.columns)-2) if i > 1]
scale[5] = round(math.sqrt(scale[6]))

    ## * Generando el DataFrame de reporte
activities_df = activities_df.reset_index()
scale_df = pd.DataFrame([scale], columns=list(activities_df.columns)[3:10])


# Calculamos los valores de la Beta-Pert
    ## Definiendo el evento aleatorio
def gen_dist():
    probabilidades = [round(random.random(), 2) for _ in range(len(activities_df))]
    Beta_Pert = stats.beta.ppf(
        probabilidades,
        activities_df['alpha'],
        activities_df['beta'],
        activities_df['Min'],
        (activities_df['Max'] - activities_df['Min']),
    )
    ans = probabilidades + list(Beta_Pert) + [round(sum(Beta_Pert))]
    return ans

    ## Generando las simulaciones
iteraciones  = range(num_interaciones)
simulaciones_ext = [gen_dist() for _ in iteraciones]

simulaciones_ext = pd.DataFrame(simulaciones_ext)
simulaciones = list(simulaciones_ext.iloc[:,-1])
print(simulaciones_ext)
print(simulaciones)