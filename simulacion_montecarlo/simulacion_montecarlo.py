import pandas as pd
import numpy as np
import matplotlib as mpl
import math
import scipy.stats as stats
import random


## Generamos el Dataframe de Entradas
activities = {
    "N": [1, 2, 3, 4, 5, 6, 7, 8],
    "Actividades": ["Actividad 1", "Actividad 2", "Actividad 3", "Actividad 4", "Actividad 5", "Actividad 6", "Actividad 7", "Actividad n"],
    "Min": [36, 27, 72, 45, 90, 63, 54, 18],
    "+Probable": [40, 30, 80, 50, 100, 70, 60, 20],
    "Max": [50, 37.5, 100, 62.5, 125, 87.5, 75, 25],
    "Ruta_Critica": [1, 0, 1, 0, 1, 0, 0, 1],
}
activities_df = pd.DataFrame(activities)
activities_df = activities_df[activities_df["Ruta_Critica"] == 1]

## Apliando el DataFrame
activities_df['Media_(µ)']  = (activities_df['Max'] + 4*activities_df['+Probable'] + activities_df['Min']) / 6
activities_df['σ']          = (activities_df['Max'] - activities_df['Min']) / 6
activities_df['σ^2']        = activities_df['σ']**2
activities_df['α']          = ((activities_df['Media_(µ)'] - activities_df['Min']) / (activities_df['Max'] - activities_df['Min'])) * (((activities_df['Media_(µ)'] - activities_df['Min']) * (activities_df['Max'] - activities_df['Media_(µ)']) / activities_df['σ']**2) - 1)
activities_df['β']          = ((activities_df['Max'] - activities_df['Media_(µ)']) / (activities_df['Media_(µ)'] - activities_df['Min'])) * activities_df['α']

print(activities_df)

## Calculamos los valores de la Beta-Pert
def gen_dist():
    probabilidades = [random.random() for _ in range(len(activities_df))]
    # probabilidades = [
    #     0.69,
    #     0.96,
    #     0.18,
    #     0.01,
    #     0.40,
    #     0.88,
    #     0.45,
    #     0.49,
    # ]

    Beta_Pert = stats.beta.ppf(
        probabilidades,
        activities_df['α'],
        activities_df['β'],
        activities_df['Min'],
        activities_df['Max'],
    )

    return probabilidades, sum(Beta_Pert)


## Generando las simulaciones
# simulaciones = [gen_dist() for _ in range(400)]
simulaciones = gen_dist()

print(simulaciones[0], simulaciones[1])