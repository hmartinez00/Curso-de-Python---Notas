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

def report(__list_steps__, __status__):
    if __status__   ==0:
        for i in __list_steps__:
            print(f'{__list_steps__[i][0]} Listo!'.replace(': ', ' - '))
    elif __status__ ==1:
        for i in __list_steps__:
            input(f'\n{__list_steps__[i][0]}\n{__list_steps__[i][1]}\n{msg_seg}\n')

while True:
    num_interaciones = input('Paso 1 - Introduzca el numero de simulaciones: ')
    if num_interaciones.isdigit():
        num_interaciones = int(num_interaciones)
        break
    else:
        print('Ingrese un número válido.')    


# Generando menu de presentacion de informe
print('\nPaso 2 - Modos de presentacion del informe:\n')
list_report_type = []
list_report_type.append('Simple')
list_report_type.append('Mostrar detalles')
list_report_type.append('Enviar a Archivo Excel')
options = range(len(list_report_type))

for i in options:
    print(f'{i}. ', list_report_type[i])

while True:
    report_type = input('\nIntroduzca el tipo de reporte que desea: ')
    if report_type.isdigit():
        if int(report_type) in options:
            report_type = int(report_type)
            break
        else:
            print('Opcion Invalida!')
    else:
        print('Ingrese un número válido.')

time_A = dt.now()

# Generamos el Dataframe de Entradas
archivo_excel = 'test.xlsx'
nombre_hoja = 'Inputs'

# Lee los datos de la hoja de cálculo en un dataframe
activities_df = pd.read_excel(archivo_excel, sheet_name=nombre_hoja)
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
scale_df = pd.DataFrame([scale], columns=list(activities_df.columns)[3:10])

activities_df = activities_df.reset_index()

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
iteraciones  = range(num_interaciones)
simulaciones = [gen_dist()[2] for _ in iteraciones]

# Generando distribucion de frecuencias
    ## Particionamos el espacio
valor_inicial = scale[0]
valor_final = scale[2]
numero_cortes = 20
particion = np.round(np.linspace(valor_inicial, valor_final, numero_cortes + 1), decimals=0).astype(int)
    ## Construimos la lista de frecuencias
def count_occurrences(__list1__, __list2__):
    count_list = []
    for element in __list1__:
        count = __list2__.count(element)
        count_list.append(count)
    return count_list

occurrences = count_occurrences(particion, simulaciones)

time_B = dt.now()
time = time_B - time_A
seconds = time.total_seconds()

# Generando reporte
print('\nPaso 3: Generando reporte')
list_steps = {}
list_steps[0] = ['\t- Inputs: ', activities_df]
list_steps[1] = ['\t- Valores acumulados de la ruta critica: ', scale_df]
list_steps[2] = ['\t- Simulaciones: ', simulaciones]
list_steps[3] = ['\t- Particion: ', particion]
list_steps[4] = ['\t- Distribucion de frecuencias: ', occurrences]
report(list_steps, report_type)

print(f'\nTiempo de calculo: {seconds}s\n')

# Generamos el grafico
# plt.style.use('dark_background')
fondo = '#161A25'
contraste = 'white'
letras = '#9598A1'
file = 'beta_pert_distribution.svg'
msg = 'Plot saved as beta_pert_distribution.svg'
labelX = 'X'
labelY = 'Probability Density'
title = f'Beta-PERT Distribution'
subtitle = f'(Iteraciones = {num_interaciones} & Tiempo: {seconds}s)'

fig, ax = plt.subplots()
x = particion
y = occurrences
plt.plot(x, y, color='red')
fig.set_facecolor(fondo)
ax.set_facecolor(fondo)
ax.set_xlabel(labelX)
ax.set_ylabel(labelY)
ax.grid(linestyle='--', alpha=0.3)
ax.tick_params(colors=letras)
ax.yaxis.label.set_color(letras)
ax.xaxis.label.set_color(letras)

ax1 = ax.twiny()
ax1.bar(x, y, edgecolor=letras, linewidth=1, width=4, facecolor='none')
ax1.tick_params(colors=letras)

# Save the plot as a PNG file
fig.subplots_adjust(top=0.84, bottom=0.15)
fig.suptitle(title, color=contraste, alpha=0.7)
plt.title(subtitle, color=contraste, alpha=0.7, fontsize=11)
fig.savefig(file, format="svg", dpi=300)

plt.close(fig)
# Display a message once the file is saved
print(msg)