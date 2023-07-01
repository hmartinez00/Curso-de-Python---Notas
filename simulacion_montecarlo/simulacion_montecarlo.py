from turtle import color
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
import random
from datetime import datetime as dt


# Generamos el Dataframe de Entradas
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

    ## Ampliamos el DataFrame
activities_df['Media_(µ)']  = (activities_df['Max'] + 4*activities_df['+Probable'] + activities_df['Min']) / 6
activities_df['σ']          = (activities_df['Max'] - activities_df['Min']) / 6
activities_df['σ^2']        =  activities_df['σ']**2
activities_df['α']          = ((activities_df['Media_(µ)'] - activities_df['Min']) / (activities_df['Max'] - activities_df['Min'])) * (((activities_df['Media_(µ)'] - activities_df['Min']) * (activities_df['Max'] - activities_df['Media_(µ)']) / activities_df['σ']**2) - 1)
activities_df['β']          = ((activities_df['Max'] - activities_df['Media_(µ)']) / (activities_df['Media_(µ)'] - activities_df['Min'])) * activities_df['α']

    ## Determinamos las sumas del DataFrame extendido
scale = [round(activities_df.iloc[:, i].sum()) for i in range(len(activities_df.columns)-2) if i > 1]
scale[5] = round(math.sqrt(scale[6]))
activities_df = activities_df.reset_index()
print(activities_df)
print(scale)

# Calculamos los valores de la Beta-Pert
def gen_dist():
    probabilidades = [round(random.random(), 2) for _ in range(len(activities_df))]
    Beta_Pert = stats.beta.ppf(
        probabilidades,
        activities_df['α'],
        activities_df['β'],
        activities_df['Min'],
        (activities_df['Max'] - activities_df['Min']),
    )
    ans = [probabilidades, Beta_Pert, round(sum(Beta_Pert))]
    return ans

# Generando las simulaciones
iteraciones = range(4000)
simulaciones, times = [gen_dist()[2] for _ in iteraciones], [dt.now() for _ in iteraciones]
time = times[-1] - times[0]
print(simulaciones)
print(time)

# Generando distribucion de frecuencias
    ## Particionamos el espacio
valor_inicial = scale[0]
valor_final = scale[2]
numero_cortes = 20
particion = np.round(np.linspace(valor_inicial, valor_final, numero_cortes + 1), decimals=0).astype(int)
print(particion)

    ## Construimos la lista de frecuencias
def count_occurrences(__list1__, __list2__):
    count_list = []
    for element in __list1__:
        count = __list2__.count(element)
        count_list.append(count)
    return count_list
occurrences = count_occurrences(particion, simulaciones)
print(occurrences)

# Generamos el grafico
x = particion
y = occurrences
plt.bar(x, y, edgecolor='blue', linewidth=1, width=4, facecolor='none')
plt.plot(x, y, color='red')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('Beta-PERT Distribution')
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('beta_pert_distribution.png')

# Display a message once the file is saved
print("Plot saved as beta_pert_distribution.png")