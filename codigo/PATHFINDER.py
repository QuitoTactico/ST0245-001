''' IMPORTANTE. Es necesario instalar PANDAS, NETWORKX, y FOLIUM desde CMD con PIP '''
#      Ejemplo: [Desde CMD] C:\Users\esteb> pip install pandas  
import pandas      #    [PANDAS]. pasa el .csv a diccionario de [PANDAS]
import networkx    #  [DIJKSTRA]. pasa el diccionario de pandas a GRAFO, para que se le pueda aplicar un [DIJKSTRA]
import folium      #[GRAFICABLE]. convierte el camino de dijkstra, en algo [GRAFICABLE] por una página, nos da su [HTML]
import os          #   [GUARDAR]. para [GUARDAR] el html
import webbrowser  #     [ABRIR]. para [ABRIR] ese html en el navegador



def DIJKSTRA_PATHFINDER(origen: tuple, destino: tuple, distancia_o_acoso : str):  # -> djk[] , Camino.html  

    #CONVERTIMOS EL .CSV EN UN DATAFRAME USANDO PANDAS
    dataframe = pandas.read_csv("calles_de_medellin_con_acoso.csv", sep=';')
    dataframe.head()  #DICCIONARIO DE PANDAS

    #LO CONVERTIMOS EN UN GRAFO
    grafo = networkx.from_pandas_edgelist(dataframe,source='origin',target='destination',edge_attr= distancia_o_acoso)

    #LE APLICAMOS PATHFINDING DE DIJKSTRA, TOMANDO EN CUENTA LO QUE SE LE INDIQUE (DISTANCIA O ACOSO)
    djk= networkx.dijkstra_path(grafo, source= str(origen), target= str(destino), weight= distancia_o_acoso)

    #IMPRIMIMOS EL CAMINO RESULTANTE DEL DIJKSTRA, Y ALGUNAS DE SUS CARACTERÍSTICAS
    print("\n[COORDENADAS RESULTANTES DEL PATHFINDING] "+distancia_o_acoso)
    print(djk)  
    if distancia_o_acoso == "length" : print("> [Terminó con un total de "+str(networkx.dijkstra_path_length(grafo,str(origen),str(destino),distancia_o_acoso))+" metros por recorrer]")
    print(">[Debes cruzar " + str(len(djk)) + " calles] "+distancia_o_acoso)

    #HAY QUE INVERTIR LAS DUPLAS (LATITUD/LONGITUD -> LONGITUD/LATITUD) 
    #PARA QUE FOLIUM PUEDA INTERPRETARLAS Y GRAFICARLAS CORRECTAMENTE.
    for i in range(len(djk)):   djk[i] = eval(djk[i])[::-1]

    #EL CAMINO CON MENOR DISTANCIA SERÁ ROJO
    #MIENTRAS QUE EL DE MEJOR ACOSO, SERÁ AZUL
    if distancia_o_acoso == "length" : diferente_color = 'red'
    if distancia_o_acoso == "harassmentRisk" : diferente_color = 'blue'

    #DEFINIMOS CUÁL SERÁ EL PUNTO CENTRAL DEL MAPA RENDERIZADO (EL ORIGEN DEL CAMINO), Y SU ZOOM
    #TAMBIÉN DEFINIMOS EL COLOR, EL GROZOR Y LA OPACIDAD DE LA LÍNEA A USAR
    mapa = folium.Map (djk[0], zoom_start = 20)
    ruta = folium.PolyLine(djk,color = diferente_color ,weight = 10,opacity = 0.8).add_to(mapa)
    
    #GUARDA EL CAMINO Y SU CONFIGURACIÓN DE RENDERIZADO EN UN HTML
    mapa.save (os.path.join('Camino.html'))

    #ABRE EL HTML EN EL NAVEGADOR
    webbrowser.open_new_tab('Camino.html')
    #Ahora puedes ver en el mapa, los caminos que hayas solicitado. c:


# ------------------------------- MÉTODOS AUXILIARES Y EJECUTORES --------------------------------


def main() -> None:
    print("\n[Para esta entrega se están utilizando orígenes y destinos de prueba].")
    print("(Ejm: Ruta entre Parque Explora, y la EAFIT)")

    print("\n> Ingrese su origen:")
    origen = menu_escoger_ubicacion()
    print("\n> Ingrese su destino:")
    destino = menu_escoger_ubicacion()

    #EL QUE REALMENTE EJECUTA EL METODO QUE CONTIENE AL DIJKSTRA
    menu_distancia_o_acoso(origen, destino)
    

def menu_escoger_ubicacion() -> tuple :
    print("0.EAFIT              5.Edificio Coltejer")
    print("1.CasaEjemplo 1      6.Estación San Antonio")
    print("2.CasaEjemplo 2      7.Parque Explora")
    print("3.CasaEjemplo 3      8.Est. Atanasio Girardot")
    print("4.CasaEjemplo 4      9.Aeropuerto Olaya Herrera")

    #¿Qué ubicación escogiste?
    num = int(input())

    #Es como un switch, solo que en python no hay
    if num == 0: return (-75.578416, 6.2007688)
    if num == 1: return (-75.583682, 6.2892842)
    if num == 2: return (-75.6123571, 6.2440634)
    if num == 3: return (-75.6090443, 6.2231431)
    if num == 4: return (-75.5387441, 6.2986144)
    if num == 5: return (-75.5664549, 6.2500233)
    if num == 6: return (-75.5697559, 6.2472846)
    if num == 7: return (-75.5635812, 6.2703451)
    if num == 8: return (-75.5879543, 6.2568545)
    if num == 9: return (-75.5887149, 6.216229)
    #default: En caso de un input inválido, retornar EAFIT
    return (-75.578416, 6.2007688)  


#EJECUTA EL PATHFINDING DE ACUERDO A LO QUE SE DESEE (Una o dos veces, y tomando qué en cuenta)
def menu_distancia_o_acoso(origen:tuple, destino:tuple) -> None:

    print("¿Desea que para la ruta se tome en cuenta la menor DISTANCIA o el menor ACOSO?\n")
    print("> Distancia / Acoso :  (o solo presione ENTER para ejecutar los dos)")

    distancia_o_acoso = str(input()).lower()

    #Otro switch. Este es el que ejecuta el código principal (Una o más veces)
    if distancia_o_acoso=="distancia" or distancia_o_acoso=="d" or distancia_o_acoso=="1": 
        print("[DISTANCIA]")
        DIJKSTRA_PATHFINDER(origen, destino, "length")
        return

    if distancia_o_acoso=="acoso" or distancia_o_acoso=="a" or distancia_o_acoso=="2": 
        print("[ACOSO]")
        DIJKSTRA_PATHFINDER(origen, destino, "harassmentRisk")
        return

    #default: Ejecuta los dos.
    print("[DISTANCIA Y ACOSO]")
    DIJKSTRA_PATHFINDER(origen, destino, "length")
    DIJKSTRA_PATHFINDER(origen, destino, "harassmentRisk")


main()



''' ---------------------------- [DIJKSTRA_PATHFINDER.PY] --------------------------------
       _          
       \`*-.
        )  _`-.        by:        ESTEBAN VERGARA GIRALDO        ඞ
       .  : `. .
       : _   '  \
       ; *` _.   `*-._             MIGUEL ANGEL COCK CANO
       `-.-'          `-.
         ;       `       `.
         :.       .        \    SEBASTIÁN CAMACHO PALACIO
         . \  .   :   .-'   .   
         '  `+.;  ;  '      :   
         :  '  |    ;       ;-.       [ENTREGA 2]
         ; '   : :`-:     _.`* ;
      .*' /  .*' ; .*`- +'  `*'
      `*-*   `*-*  `*-*'

    _                ___       _.--.
    \`.|\..----...-'`   `-._.-'_.-'`    -------- REQUERIMIENTOS: -----------------
    /  ' `         ,       _.-'               calles_de_medellin_con_acoso.csv
    )/' _/     \   `-_,   /                poligono_de_medellin.csv
    `-'" `"\_  ,_.-;_.-\_ ',            PANDAS
        _.-'_./   {_.'   ; /         NETWORKX       <- INSTALL WITH PIP (CMD)
       {_.-``-'         {_/       FOLIUM
       '''                               