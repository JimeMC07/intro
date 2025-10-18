import tkinter as tk
from tkinter import *

def juego():
    ventana_principal.withdraw()
    ventana_juego = tk.Toplevel() 
    ventana_juego.title("Juego") 
    ventana_principal.config(bg="lightblue")

    ancho_ventana =  ventana_juego.winfo_screenwidth() 
    alto_ventana = ventana_juego.winfo_screenheight()
    ventana_juego.geometry(f"{ancho_ventana}x{alto_ventana}")

    ancho_canvas = (ventana_juego*0.8) // 100
    alto_canvas = (ventana_juego*0.8) // 100

    canvas_juego = Canvas(ventana_juego, width=ancho_canvas, height=alto_canvas, bg="black")
    canvas_juego.pack()

 

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

