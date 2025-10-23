import tkinter as tk
from tkinter import *
import random

def juego():
    #ventana_principal.withdraw()
    ventana_juego = tk.Toplevel() 
    ventana_juego.title("Juego") 
    ventana_principal.config(bg="lightblue")

    ancho_ventana =  ventana_juego.winfo_screenwidth() 
    alto_ventana = ventana_juego.winfo_screenheight()

    ventana_juego.geometry(f"{ancho_ventana}x{alto_ventana}")

    ancho_can = int(ancho_ventana * 0.8) // 40 * 40
    alto_can = int(alto_ventana * 0.8) // 40 * 40

    print(ancho_can)
    print(alto_can)

    can_juego = Canvas(ventana_juego, width=ancho_can, height=alto_can, bg="black")
    can_juego.pack()

    
    can_juego.jugador = crear_personaje(can_juego, 640, 360)
    can_juego.bind_all("<KeyPress>", lambda event: mover_jugador(can_juego, event, 20, ancho_can, alto_can))
    can_juego.ultima_direccion = "arriba"

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

    x1, y1, x2, y2 = can.coords(can.jugador)
    
    """nx = x + movimiento_x
    ny = y + movimiento_y"""

    can.move(can.jugador, movimiento_x, movimiento_y)
    fuera_pantalla(can, can.jugador, ancho_can, alto_can)


#Función para detectar que salió fuera de la pantalla el jugador
#############################################################################
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


    pos_moto1 = can.coords(bola_roja)
    pos_moto2 = can.coords(bola_azul)

    #Valorar si las esferas rebotan en los bordes

    #Bola Roja
    if pos_moto1[3] >= 300 or pos_moto1[1] <= 0:
        ventana.vel_rojo[1] = -ventana.vel_rojo[1]

    if pos_moto1[2] >= 400 or pos_moto1[0] <= 0:
        ventana.vel_rojo[0] = -ventana.vel_rojo[0]


    #Bola azul
    if pos_moto2[3] >= 300 or pos_moto2[1] <= 0:
        ventana.vel_azul[1] = -ventana.vel_azul[1]
        
    if pos_moto2[2] >= 400 or pos_moto2[0] <= 0:
        ventana.vel_azul[0] = -ventana.vel_azul[0]


    #Valorar si las esferas rebotan entre ellas

    if (pos_moto1[0] < pos_moto2[2] and
        pos_moto1[2] > pos_moto2[0] and
        pos_moto1[1] < pos_moto2[3] and
        pos_moto1[3] > pos_moto2[1]):

        ventana.vel_rojo[0] = -ventana.vel_rojo[0]
        ventana.vel_rojo[1] = -ventana.vel_rojo[1]
        ventana.vel_azul[0] = -ventana.vel_azul[0]
        ventana.vel_azul[1] = -ventana.vel_azul[1]

    ventana.after(20, AnimacionRecursiva, can, bola_roja, bola_azul, ventana)"""

#Ventana Principal
#########################################################################################
ventana_principal = tk.Tk() #Estoy creando la ventana principal, eso significa Tk
ventana_principal.title("Taller tkinter") #Le da nombre a la ventana


ancho_ventana =  ventana_principal.winfo_screenwidth() 
alto_ventana = ventana_principal.winfo_screenheight() 

ventana_principal.geometry(f"{ancho_ventana}x{alto_ventana}") #Ajusta los margenes y la posicion de donde aparece de la ventana
ventana_principal.config(bg="lightblue")

boton_animación = Button(ventana_principal, text= "Jugar", command=juego, width= 30, height= 3, bg= "pink", fg= "black") # crea el boton con diferentes atributos y lo que va a hacer
boton_animación.place(x=300, y=100) #posiciona el boton dentro de la ventana

ventana_principal.mainloop() #funcion de loop(bucle) para mantener la ventana abierta


