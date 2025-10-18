import tkinter as tk
from tkinter import *

def juego():
    #ventana_principal.withdraw()
    ventana_juego = tk.Toplevel() 
    ventana_juego.title("Juego") 
    ventana_principal.config(bg="lightblue")

    ancho_ventana =  ventana_juego.winfo_screenwidth() 
    alto_ventana = ventana_juego.winfo_screenheight()

    ventana_juego.geometry(f"{ancho_ventana}x{alto_ventana}")

    ancho_canvas = int(ancho_ventana * 0.8) // 40 * 40
    alto_canvas = int(alto_ventana * 0.8) // 40 * 40

    print(ancho_canvas)
    print(alto_canvas)

    canvas_juego = Canvas(ventana_juego, width=ancho_canvas, height=alto_canvas, bg="black")
    canvas_juego.pack()

    
    canvas_juego.jugador = crear_personaje(canvas_juego, 640, 360)
    canvas_juego.bind_all("<KeyPress>", lambda event: mover_jugador(canvas_juego, event, 20, ancho_canvas, alto_canvas))
    canvas_juego.ultima_direccion = "arriba"

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
    ancho_obj = x2 - x1
    alto_obj = y2 - y1

    if x2 < 0:
        can.coords(objeto, ancho - ancho_obj, y1, ancho, y2)

    elif x1 > ancho:
        can.coords(objeto, 0, y1, ancho_obj, y2)

    elif y2 < 0:
        can.coords(objeto, x1, alto - alto_obj, x2, alto)

    elif y1 > alto:
        can.coords(objeto, x1, 0, x2, alto_obj)


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


