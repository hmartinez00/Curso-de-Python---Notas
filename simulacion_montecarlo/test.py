import pandas as pd

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

# Especifica el nombre del archivo Excel y el nombre de la hoja
archivo_excel = 'test.xlsx'
nombre_hoja = 'Inputs'

# Exporta el DataFrame a un archivo de Excel con el nombre de la hoja
activities_df.to_excel(archivo_excel, sheet_name=nombre_hoja, index=False)

print("El DataFrame se ha exportado exitosamente a un archivo de Excel.")