import pandas # Para creación, lectura y manejo de dataframes

#[LECTURA] Leer el csv
dataframe = pandas.read_csv("calles_de_medellin_con_acoso.csv", sep=';')
print("\n1. Pasamos de esto:\n",dataframe)

#[FILTRADO] Tomar de él solamente las columnas estrictamente necesarias
dataframe = dataframe[["origin","destination","length","harassmentRisk"]]
print("\n\n2. A solo estas 4 columnas, las importantes:\n",dataframe)

#[CÁLCULO] Deducir el promedio de acoso
suma_de_acosos = dataframe["harassmentRisk"].sum()
numero_de_datos = len(dataframe) - dataframe["harassmentRisk"].isna().sum()
promedio_de_acoso = suma_de_acosos / numero_de_datos  # 68749 es el número de calles que tenemos.
                                                      # réstale las que no tenían datos de acoso, que son 16091
                                                      # divide la sumatoria (44417.43) por ese número (52658)
                                                      # 44417.43 / 52658 = 0.8435078086511826
                                                      # ese es el promedio, úsalo para rellenar

#[COMPLETAR] Rellenar NaN con ese promedio
dataframe["original_harassmentRisk"] = dataframe["harassmentRisk"]
dataframe["harassmentRisk"] = dataframe["harassmentRisk"].fillna(value = promedio_de_acoso)
print("\n\n3. Rellenamos los valores NaN de acoso con el promedio de los que teníamos (",promedio_de_acoso,"):\n",dataframe)

#[MULTIPLICAR] Crear nueva columna
dataframe["length_multiplied_by_harassment"] = dataframe["length"] * dataframe["harassmentRisk"] 

#[POTENCIAR] Otra columna más, una relación diferente entre las variables
dataframe["length_powered_by_harassment"] = dataframe["length"] ** dataframe["harassmentRisk"] 
print("\n\n4. Y finalmente tenemos nuestras nuevas columnas  :)\n",dataframe)

#[GUARDADO] Guardar datos finales a usar.
dataframe.to_csv('FINAL_DATA.csv', sep=';', index=False)

print("\n\n5. Por cierto, el promedio de acoso en colombia es de: ",promedio_de_acoso,"\n   Da pena")
print("\nMira tus archivos, los datos finales que usaremos ya deben de estar allí.")
print("                        >> FINAL_DATA.csv <<\n")
