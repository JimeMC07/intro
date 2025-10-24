import tkinter as tk
from tkinter import *
import random
import os
from PIL import Image, ImageTk


def Carga_de_Imagenes_Escaladas(nombre, px1, px2):
    ruta = os.path.join(r'C:\Users\ricar\Desktop\Proyecto Intro Jimena\intro\imagenes', nombre)
    
    imagen_original = Image.open(ruta)  
    imagen_escalada = imagen_original.resize((px1, px2), Image.Resampling.LANCZOS)  
    imagen_final = ImageTk.PhotoImage(imagen_escalada) 
    
    return imagen_final

def juego():
    #ventana_principal.withdraw()
    ventana_juego = tk.Toplevel() 
    ventana_juego.title("Juego") 

    ancho_ventana =  ventana_juego.winfo_screenwidth() 
    alto_ventana = ventana_juego.winfo_screenheight()

    ventana_juego.geometry(f"{ancho_ventana}x{alto_ventana}")

    imagen = Carga_de_Imagenes_Escaladas("fondo_juego.png", ancho_ventana, alto_ventana)
    Imagen_fondo_juego = Label(ventana_juego, image = imagen) #Crea una etiqueta con la imagen de fondo
    Imagen_fondo_juego.place(x=0, y=0, relwidth=1, relheight=1) #posiciona la imagen de fondo en la ventana

    ventana_juego.imagen_fondo = imagen

    ancho_canvas = int(ancho_ventana * 0.8) // 40 * 40
    alto_canvas = int(alto_ventana * 0.8) // 40 * 40

    canvas_juego = Canvas(ventana_juego, width=ancho_canvas, height=alto_canvas, bg="black")
    canvas_juego.pack()

    #Cargar imagenes moto rosa
    imagen_rosa1 = Carga_de_Imagenes_Escaladas("rosa1.png", 40, 40)
    canvas_juego.imagen_rosa1 = imagen_rosa1
    imagen_rosa2 = Carga_de_Imagenes_Escaladas("rosa2.png", 40, 40)
    canvas_juego.imagen_rosa2 = imagen_rosa2
    imagen_rosa3 = Carga_de_Imagenes_Escaladas("rosa3.png", 40, 40)
    canvas_juego.imagen_rosa3 = imagen_rosa3

    #Cargar imagenes moto azul
    imagen_azul1 = Carga_de_Imagenes_Escaladas("azul1.png", 40, 40)
    canvas_juego.imagen_azul1 = imagen_azul1    
    imagen_azul2 = Carga_de_Imagenes_Escaladas("azul2.png", 40, 40)
    canvas_juego.imagen_azul2 = imagen_azul2
    imagen_azul3 = Carga_de_Imagenes_Escaladas("azul3.png", 40, 40)
    canvas_juego.imagen_azul3 = imagen_azul3

    #Cargar imagenes moto verde
    imagen_verde1 = Carga_de_Imagenes_Escaladas("verde1.png", 40, 40)
    canvas_juego.imagen_verde1 = imagen_verde1      
    imagen_verde2 = Carga_de_Imagenes_Escaladas("verde2.png", 40, 40)
    canvas_juego.imagen_verde2 = imagen_verde2
    imagen_verde3 = Carga_de_Imagenes_Escaladas("verde3.png", 40, 40)
    canvas_juego.imagen_verde3 = imagen_verde3
    
    canvas_juego.jugador = crear_personaje(canvas_juego, 640, 360, imagen_azul1)
    canvas_juego.bind_all("<KeyPress>", lambda event: mover_jugador(canvas_juego, event, 20, ancho_canvas, alto_canvas))
    canvas_juego.ultima_direccion = "arriba"


#Ventana apariencia
def ventana_apariencia():
    ventana_apariencia = tk.Toplevel() 
    ventana_apariencia.title("cambiar apariencia") 

    ancho_ventana =  ventana_apariencia.winfo_screenwidth() 
    alto_ventana = ventana_apariencia.winfo_screenheight()

    ventana_apariencia.geometry(f"{ancho_ventana}x{alto_ventana}")

    imagen = Carga_de_Imagenes_Escaladas("fondo_juego.png", ancho_ventana, alto_ventana)
    Imagen_fondo_juego = Label(ventana_apariencia, image = imagen) #Crea una etiqueta con la imagen de fondo
    Imagen_fondo_juego.place(x=0, y=0, relwidth=1, relheight=1) #posiciona la imagen de fondo en la ventana

    ventana_apariencia.imagen_fondo = imagen

#################################################################################

#Bloque de funciones 
#################################################################################
#################################################################################


#Crear Personaje
######################################################################
def crear_personaje(can, x, y, moto):
    return can.create_image(x, y, image=moto)


#Mover Jugador
######################################################################
def mover_jugador(can, event, velocidad, ancho_can, alto_can):
    movimiento_x = 0
    movimiento_y = 0

    if event.keysym == 'a':
        movimiento_x = -velocidad
        can.ultima_direccion = "izquierda"
        
    elif event.keysym == 'd':
        movimiento_x = velocidad
        can.ultima_direccion = "derecha"
        
    elif event.keysym == 'w':
        movimiento_y = -velocidad
        can.ultima_direccion = "arriba"
        
    elif event.keysym == 's':
        movimiento_y = velocidad
        can.ultima_direccion = "abajo"
    
    """nx = x + movimiento_x
    ny = y + movimiento_y"""

    can.move(can.jugador, movimiento_x, movimiento_y)
    fuera_pantalla(can, can.jugador, ancho_can, alto_can)


#Función para detectar que salió fuera de la pantalla el jugador
#############################################################################
def fuera_pantalla(can, objeto, ancho, alto):
    x, y = can.coords(objeto)
    
    bbox = can.bbox(objeto)

    if bbox:
        x1, y1, x2, y2 = bbox
        mitad_ancho = (x2 - x1) / 2
        mitad_alto = (y2 - y1) / 2
    else:
        mitad_ancho = 20
        mitad_alto = 20
        
    nueva_x = x
    nueva_y = y
    

    if x + mitad_ancho < 0:  
        nueva_x = ancho + mitad_ancho 
        
    elif x - mitad_ancho > ancho:  
        nueva_x = -mitad_ancho  
    

    if y + mitad_alto < 0:  
        nueva_y = alto + mitad_alto 
        
    elif y - mitad_alto > alto: 
        nueva_y = -mitad_alto  
    
    if nueva_x != x or nueva_y != y:
        can.coords(objeto, nueva_x, nueva_y)


#Función para crear a los personajes
##############################################################################
def crear_enemigos(can, nivel):

    x = random.randint(40, 1160)
    y = random.randint(40, 640)

    if nivel == 1:  
        imagen = can.imagen_rosa1
        velocidad = 5
    elif nivel == 2:
        imagen = can.imagen_azul1
        velocidad = 5
    elif nivel == 3:
        imagen = can.imagen_verde1
        velocidad = 5
    else:
        return 

    can.moto = crear_personaje(can, x, y, imagen)
    
    return can.moto
    
    """if random.choice([True, False]):
        vel_x = random.choice([-velocidad, velocidad])
        vel_y = 0
    else:
        vel_x = 0
        vel_y = random.choice([-velocidad, velocidad])"""

#Función para mover la moto
########################################################################
"""def mover_moto(can, moto_1, moto_2, moto_3, x, y):

    can.move(moto_1, x, y)
    can.move(moto_2, x, y)
    can.move(moto_3, x, y)


    pos_moto1 = can.coords(moto_1)
    pos_moto2 = can.coords(moto_2)
    pos_moto3 = can.coords(moto_3)

    
    #Valorar si las esferas rebotan entre ellas

    if (pos_moto1[0] < pos_moto2[2] and
        pos_moto1[2] > pos_moto2[0] and
        pos_moto1[1] < pos_moto2[3] and
        pos_moto1[3] > pos_moto2[1]):



    ventana.after(20, AnimacionRecursiva, can, bola_roja, bola_azul, ventana)"""

#Ventana Principal
#########################################################################################
ventana_principal = tk.Tk() #Estoy creando la ventana principal, eso significa Tk
ventana_principal.title("Taller tkinter") #Le da nombre a la ventana


ancho_ventana =  ventana_principal.winfo_screenwidth() 
alto_ventana = ventana_principal.winfo_screenheight() 
ventana_principal.geometry(f"{ancho_ventana}x{alto_ventana}") #Ajusta los margenes y la posicion de donde aparece de la ventana

imagen = Carga_de_Imagenes_Escaladas("fondo_juego.png", ancho_ventana, alto_ventana)
Imagen_fondo = Label(ventana_principal, image = imagen) #Crea una etiqueta con la imagen de fondo
Imagen_fondo.place(x=0, y=0) #posiciona la imagen de fondo en la ventana

boton_animación = Button(ventana_principal, text= "Jugar", font= ("arial", 15), command=juego, width= 40, height= 2, bg= "#5A9DB2", fg= "black") # crea el boton con diferentes atributos y lo que va a hacer
boton_animación.place(x=550, y=200) #posiciona el boton dentro de la ventana

boton_apariencia = Button(ventana_principal, text= "Apariencia", font= ("arial", 10), command=ventana_apariencia, width= 20, height= 2, bg= "#5A9DB2", fg= "black") # crea el boton con diferentes atributos y lo que va a hacer
boton_apariencia.place(x=50, y=50) #posiciona el boton dentro de la ventana

ventana_principal.mainloop() #funcion de loop(bucle) para mantener la ventana abierta


