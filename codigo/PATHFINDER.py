''' IMPORTANTE. Es necesario instalar PANDAS, NETWORKX, y FOLIUM desde CMD con PIP '''
#      Ejemplo: [Desde CMD] C:\Users\esteb> pip install pandas  
import pandas      #    [PANDAS]. pasa el .csv a diccionario de [PANDAS]
import networkx    #  [DIJKSTRA]. pasa el diccionario de pandas a GRAFO, para que se le pueda aplicar un [DIJKSTRA]
import folium      #[GRAFICABLE]. convierte el camino de dijkstra, en algo [GRAFICABLE] por una página, nos da su [HTML]
import os          #   [GUARDAR]. para [GUARDAR] el html
import webbrowser  #     [ABRIR]. para [ABRIR] ese html en el navegador

#                                                                           ÍNDICE:    DIJKSTRA_PATHFINDER         19
#                                |                                                     MAIN                        93
#                                |                                                     MENU_ESCOGER_UBICACION     129
#                                V                                                     MENU_DISTANCIA_Y_O_ACOSO   172
#    ABAJO CONVERTIREMOS EL .CSV EN UN DATAFRAME USANDO PANDAS  (Línea 325)            EJECUTOR                   194
'''  dataframe = pandas.read_csv("FINAL_DATA.csv", sep=';')  ''' #                     MAPA_DE_CALOR              240
#                                                                                      GENERAR_FINAL_DATA         280
#                                                                                      Inicializador Dataframe    325
#                                                                                      Créditos y Requerimientos  337

def DIJKSTRA_PATHFINDER(dataframe: pandas.DataFrame, origen: tuple, destino: tuple, distancia_y_o_acoso : str):  # -> djk[] , Camino.html  

    dataframe.head()  #DATAFRAME DE PANDAS CON ESTOS PARÁMETROS:
    #    origin;destination  |  length  |  harassmentRisk  |  original_harassmentRisk
    #         length_multiplied_by_harassment  |  length_powered_by_harassment

    #LO CONVERTIMOS EN UN GRAFO
    grafo = networkx.from_pandas_edgelist(dataframe,source='origin',target='destination',edge_attr= distancia_y_o_acoso)

    #LE APLICAMOS PATHFINDING DE DIJKSTRA, TOMANDO EN CUENTA LO QUE SE LE INDIQUE (DISTANCIA O ACOSO)
    djk= networkx.dijkstra_path(grafo, source= str(origen), target= str(destino), weight= distancia_y_o_acoso)

    #IMPRIMIMOS EL CAMINO RESULTANTE DEL DIJKSTRA, Y ALGUNAS DE SUS CARACTERÍSTICAS
    print("\n[COORDENADAS RESULTANTES DEL PATHFINDING] ("+distancia_y_o_acoso+") :")
    print(djk)  

    #DATOS ACERCA DE LA RUTA
    longitud = networkx.dijkstra_path_length(grafo,str(origen),str(destino),distancia_y_o_acoso)
    try:
        int(longitud)  #PARA COMPROBAR SI ES ALGÚN TIPO DE NaN
        if distancia_y_o_acoso in ["length","length_powered_by_harassment"]:
            print("> [Terminó con un total de "+str(longitud)+" metros por recorrer, unos "+str(int(longitud/1000))+" kilómetros]")
        else: print("> [Terminó con un promedio de acoso de "+str(longitud/len(djk))+"]")
    except:print("> [Imposible saber la distancia de acoso original, arroja valores NaN]")
    print("> [Debes cruzar " + str(len(djk)) + " calles] ("+distancia_y_o_acoso+")\n")

    #HAY QUE INVERTIR LAS DUPLAS (LATITUD/LONGITUD -> LONGITUD/LATITUD) 
    #PARA QUE FOLIUM PUEDA INTERPRETARLAS Y GRAFICARLAS CORRECTAMENTE.
    for i in range(len(djk)):   djk[i] = eval(djk[i])[::-1]

    #EL CAMINO CON MENOR DISTANCIA SERÁ ROJO
    #MIENTRAS QUE EL DE MEJOR ACOSO, SERÁ AZUL
    if distancia_y_o_acoso == "length" : diferente_color = 'red'
    if distancia_y_o_acoso == "harassmentRisk" : diferente_color = 'blue'
    if distancia_y_o_acoso == "original_harassmentRisk" : diferente_color = 'blue'
    if distancia_y_o_acoso == "length_multiplied_by_harassment" : diferente_color = 'green' 
    if distancia_y_o_acoso == "length_powered_by_harassment" : diferente_color = 'purple'

    #DEFINIMOS CUÁL SERÁ EL PUNTO CENTRAL DEL MAPA RENDERIZADO (EL ORIGEN DEL CAMINO), Y SU ZOOM
    #TAMBIÉN DEFINIMOS EL COLOR, EL GROZOR Y LA OPACIDAD DE LA LÍNEA A USAR
    mapa = folium.Map ([(origen[1]+destino[1])/2 , (origen[0]+destino[0])/2], zoom_start = "14")
    if distancia_y_o_acoso != "original_harassmentRisk" : 
        ruta = folium.PolyLine(djk,color = diferente_color ,weight = 10,opacity = 0.8).add_to(mapa)
    else: ruta = folium.PolyLine(djk,color = diferente_color ,weight = 10,opacity = 0.5, dash_array = 15).add_to(mapa)

    #AÑADE UNA DESCRIPCIÓN A LA RUTA, CREA SU LEYENDA
    formato = '<span style="color: {color};">{nombre_ruta}</span>'
    folium.FeatureGroup(name= formato.format( nombre_ruta= distancia_y_o_acoso.upper(), color= diferente_color)).add_to(mapa)

    #POR ALGUNA RAZÓN HAY QUE HACERLA VISIBLE, SU DEFAULT ES ESTAR OCULTA
    folium.map.LayerControl('topright', collapsed= False).add_to(mapa)

    #GUARDA EL CAMINO Y SU CONFIGURACIÓN DE RENDERIZADO EN UN HTML
    mapa.save (os.path.join('Camino.html'))

    #ABRE EL HTML EN EL NAVEGADOR
    webbrowser.open_new_tab('Camino.html')
    #Ahora puedes ver en el mapa, los caminos que hayas solicitado. c:

    #Y retoramos este, para agregarlo al mapa general
    return ruta






# ------------------------------- MÉTODOS AUXILIARES Y EJECUTORES --------------------------------






def MAIN(dataframe: pandas.DataFrame) -> None:
    print("\nDeseo...")
    print("1. HACER PATHFINDING")
    print("2. VER EL MAPA DE CALOR")
    print("3. GENERAR FINAL_DATA.CSV")

    funcion = input()
    if funcion == "2": 
        print("\nOk!\nJust, wait...")
        MAPA_DE_CALOR(dataframe,"harassmentRisk","ACOSO")
        MAPA_DE_CALOR(dataframe,"length_multiplied_by_harassment","DISTANCIA Y ACOSO MULTIPLICADOS")
        MAPA_DE_CALOR(dataframe,"length_powered_by_harassment","DISTANCIA Y ACOSO POTENCIADOS")
        quit()

    if funcion == "3":  GENERAR_FINAL_DATA()

    #DEFAULT: Ejecutar el Pathfinding
    print("\n[Para esta entrega se están utilizando orígenes y destinos de prueba].")
    print("(Ejm: Ruta entre Parque Explora, y la EAFIT)")

    print("\n> Ingrese su origen:")
    origen = MENU_ESCOGER_UBICACION()
    print("\n> Ingrese su destino:")
    destino = MENU_ESCOGER_UBICACION()
    
    #PARA SABER QUÉ QUIERE VER EL USUARIO
    distancia_y_o_acoso = MENU_DISTANCIA_Y_O_ACOSO()

    #EL QUE REALMENTE EJECUTA LAS FUNCIONES DIJKSTRA
    EJECUTOR(dataframe, origen, destino, distancia_y_o_acoso)
    





def MENU_ESCOGER_UBICACION() -> tuple :
    print("1.Universidad EAFIT             6.Edificio Coltejer          11.Robledo      ")
    print("2.Universidad de Medellín       7.Estación San Antonio       12.Laureles     ")
    print("3.Universidad de Antioquia      8.Parque Explora             13.San Cristóbal")
    print("4.Universidad Nacional          9.Est Atanasio Girardot      14.Santo Domingo")
    print("5.Universidad Luis Amigó       10.Aeropuerto O. Herrera      15.Prado        ")
    print("                     >> 0. UBICACIÓN PERSONALIZADA <<")

    #¿Qué ubicación escogiste?
    num = int(input())

    #Es como un switch, solo que en python no hay

    if num == 0:
        coords = input()
        if coords[0] != "(": coords = "("+coords+")"
        return eval(coords) if coords[1]=="-" else eval(coords)[::-1]

    if num == 1: return (-75.578416, 6.2007688)
    if num == 2: return (-75.6101004, 6.2312125)
    if num == 3: return (-75.5694416, 6.2650137)
    if num == 4: return (-75.5762232, 6.266327)
    if num == 5: return (-75.5832559, 6.2601878)

    if num == 6: return (-75.5664549, 6.2500233)
    if num == 7: return (-75.5697559, 6.2472846)
    if num == 8: return (-75.5635812, 6.2703451)
    if num == 9: return (-75.5879543, 6.2568545)
    if num == 10: return (-75.5887149, 6.216229)

    if num == 11: return (-75.583682, 6.2892842)
    if num == 12: return (-75.6123571, 6.2440634)
    if num == 13: return (-75.6371302, 6.2793696)
    if num == 14: return (-75.5387441, 6.2986144)
    if num == 15: return (-75.5575788, 6.2596423)
    #default: En caso de un input inválido, retornar EAFIT
    else: return (-75.578416, 6.2007688)  






def MENU_DISTANCIA_Y_O_ACOSO() -> str :
    print("\n> ¿Qué desea que se tome en cuenta para la mejor ruta?\n")
    print("1.     Solo Distancia    ")
    print("2.       Solo Acoso      ")
    print("3. Solo Distancia * Acoso")
    print("0.       >> TODO <<      ")

    #¿Qué búsqueda escogiste?
    num = input().lower()

    #Otro Switch
    #if num == 0: return "TODO"
    if num in ["1","d","distancia","l","length"]: return "DISTANCIA"
    if num in ["2","a","acoso","h","harassment"]: return "ACOSO"
    if num in ["3","b","ambos","both"]: return "AMBOS"
    else: return "TODO" #default






#EJECUTA EL PATHFINDING DE ACUERDO A LO QUE SE DESEE (Una o más veces, y tomando qué en cuenta)
def EJECUTOR(dataframe: pandas.DataFrame, origen:tuple, destino:tuple, distancia_y_o_acoso : str) -> None:

    print("\n["+distancia_y_o_acoso+"]")

    #Inicializa el mapa por default
    mapa = folium.Map ([(origen[1]+destino[1])/2 , (origen[0]+destino[0])/2], zoom_start = "14")
    formato = '<span style="color: {color};">{nombre_ruta}</span>'
    folium.Marker([origen[1],origen[0]], popup='Origen', tooltip='Origen').add_to(mapa)
    folium.Marker([destino[1],destino[0]], popup='Destino', tooltip='Destino').add_to(mapa)

    #De acuerdo a la respuesta del anterior switch. Este es el que ejecuta el código principal (Una o más veces)
    if distancia_y_o_acoso in ["DISTANCIA", "TODO"]: 
        print("\n>> DISTANCIA")
        DIJKSTRA_PATHFINDER(dataframe, origen, destino, "length").add_to(mapa)
        folium.FeatureGroup(name= formato.format( nombre_ruta= ' DISTANCIA', color= "red")).add_to(mapa)

    if distancia_y_o_acoso in ["ACOSO", "TODO"]: 
        print("\n>> ACOSO")
        DIJKSTRA_PATHFINDER(dataframe, origen, destino, "harassmentRisk").add_to(mapa)
        folium.FeatureGroup(name= formato.format( nombre_ruta= ' ACOSO', color= "blue")).add_to(mapa)
        print("\n>> ACOSO ORIGINAL")
        try:
            DIJKSTRA_PATHFINDER(dataframe, origen, destino, "original_harassmentRisk").add_to(mapa)
            folium.FeatureGroup(name= formato.format( nombre_ruta= ' ACOSO ORIGINAL', color= "darkblue")).add_to(mapa)
        except: print("El camino de acoso antiguo hubiera fallado por error en los datos\n")

    if distancia_y_o_acoso in ["AMBOS", "TODO"]: 
        print("\n>> DISTANCIA multiplicada por ACOSO")
        DIJKSTRA_PATHFINDER(dataframe, origen, destino, "length_multiplied_by_harassment").add_to(mapa)
        folium.FeatureGroup(name= formato.format( nombre_ruta= ' DISTANCIA * ACOSO', color= "green")).add_to(mapa)
        print("\n>> DISTANCIA potenciada por ACOSO")
        DIJKSTRA_PATHFINDER(dataframe, origen, destino, "length_powered_by_harassment").add_to(mapa)
        folium.FeatureGroup(name= formato.format( nombre_ruta= ' DISTANCIA ^ ACOSO', color= "purple")).add_to(mapa)
    #default: Ejecuta todo.

    #Guarda la leyenda, el mapa, y los abre en el navegador
    folium.map.LayerControl('topright', collapsed= False).add_to(mapa)
    mapa.save (os.path.join('Camino_all.html'))
    webbrowser.open_new_tab('Camino_all.html')






def MAPA_DE_CALOR(dataframe: pandas.DataFrame, tipo_de_acoso:str, titulo:str):

    #Convertir las latitudes y longitudes en listas individuales
    longitudes = [eval(calle)[0] for calle in dataframe["origin"]]
    latitudes = [eval(coord)[1] for coord in dataframe["origin"]]
    
    #Inicializar un objeto de mapa
    mapa_calor = folium.Map(location=[6.251994, -75.572947], zoom_start = 14.5)
    
    
    #Por alguna razón folium no permite utilizar HeatMap directamente
    #Sin embargo, crear una capa de mapa de calor es más fácil de lo que creía
    from folium.plugins import HeatMap

    #Zip agrupa las iteraciones de cada lista como si las convirtiera en una colección
    #Los rangos que se crean entre estas "colecciones" según el acoso, es lo que graficaremos
    HeatMap(list(zip(latitudes, longitudes, dataframe[tipo_de_acoso])),
                      min_opacity=0.2, radius=30, blur=20, max_zoom=1).add_to(mapa_calor)

    #También podemos agregarle una barra guía de colores, para hacerlo más ilustrativo
    import branca                             #Escogemos los colores y el intervalo de cambio
    colormap = branca.colormap.LinearColormap(['blue','green', 'yellow','orange', 'red'], vmin=0, vmax=1)
    colormap = colormap.to_step(index=[0, 0.1, 0.2 ,0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    colormap.caption = '[ '+titulo+' ]'  #Le ponemos un título
    colormap.add_to(mapa_calor)               #Y lo guardamos como todos los objetos anteriores

    #Importamos esto para agregarle una imagen de referencia de medellín en una esquina al HeatMap
    from folium.plugins import FloatImage
    image_file = 'Medellin.png'
    FloatImage(image_file, bottom=3, left=3).add_to(mapa_calor)

    #Le añadimos la capa creada al mapa, y lo guardamos para abrirlo como siempre
    mapa_calor.save (os.path.join('Heat.html'))
    webbrowser.open_new_tab('Heat.html')






def GENERAR_FINAL_DATA():

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
    return dataframe






#CONVERTIMOS EL .CSV EN UN DATAFRAME USANDO PANDAS
try:     dataframe = pandas.read_csv("FINAL_DATA.csv", sep=';')         #Inicializador Dataframe
except:  dataframe = GENERAR_FINAL_DATA()


MAIN(dataframe)








''' ---------------------------- [DIJKSTRA_PATHFINDER.PY] --------------------------------
       _          
       \`*-.
        )  _`-.        by:        ESTEBAN VERGARA GIRALDO        ඞ 
       .  : `. .
       : _   '  \
       ; *` _.   `*-._            MIGUEL ANGEL COCK CANO
       `-.-'          `-.
         ;       `       `.
         :.       .        \     SEBASTIÁN CAMACHO PALACIO
         . \  .   :   .-'   .   
         '  `+.;  ;  '      :   
         :  '  |    ;       ;-.        [ENTREGA 2]
         ; '   : :`-:     _.`* ;
      .*' /  .*' ; .*`- +'  `*'
      `*-*   `*-*  `*-*'

    _                ___       _.--.    ----------- REQUERIMIENTOS: --------------
    \`.|\..----...-'`   `-._.-'_.-'`             calles_de_medellin_con_acoso.csv
    /  ' `         ,       _.-'               poligono_de_medellin.csv
    )/' _/     \   `-_,   /                GENERAR_FINAL_DATA.py
    `-'" `"\_  ,_.-;_.-\_ ',            FINAL_DATA.csv
        _.-'_./   {_.'   ; /         NETWORKX     
       {_.-``-'         {_/       PANDAS         <- INSTALL WITH PIP (CMD)
                               FOLIUM  
                            '''