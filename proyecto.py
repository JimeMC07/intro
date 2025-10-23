import tkinter as tk
from tkinter import *
import os
from PIL import Image, ImageTk


def Carga_de_Imagenes_Escaladas(nombre, px1, px2):
    ruta = os.path.join(r'C:\Users\Jimen\Desktop\TEC\Segundo Semestre\Intro 2\proyecto intro\intro\imagenes', nombre)
    
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
    
    canvas_juego.jugador = crear_personaje(canvas_juego, 640, 360)
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
def crear_personaje(can, x, y):
    return can.create_oval(10, 10, 60, 60, fill="skyblue", outline="black", width=2)
    #return can.create_image(x, y)


#Mover Jugador
######################################################################
def mover_jugador(can, event, velocidad, ancho_canvas, alto_canvas):
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

    x1, y1, x2, y2 = can.coords(can.jugador)
    
    """nx = x + movimiento_x
    ny = y + movimiento_y"""

    can.move(can.jugador, movimiento_x, movimiento_y)
    fuera_pantalla(can, can.jugador, ancho_canvas, alto_canvas)


def fuera_pantalla(can, objeto, ancho, alto):
    x1, y1, x2, y2 = can.coords(objeto)
    ancho_objeto = x2 - x1
    alto_objeto = y2 - y1

    if x2 < 0:
        can.coords(objeto, ancho - ancho_objeto, y1, ancho, y2)

    elif x1 > ancho:
        can.coords(objeto, 0, y1, ancho_objeto, y2)

    elif y2 < 0:
        can.coords(objeto, x1, alto - alto_objeto, x2, alto)

    elif y1 > alto:
        can.coords(objeto, x1, 0, x2, alto_objeto)


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


