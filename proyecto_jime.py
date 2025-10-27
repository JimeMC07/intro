########################################################### Aquí van los imports y configuracciones importantes ############################################################

#----Imports----#
import tkinter as tk
from tkinter import *
from tkinter import messagebox  # agregado para Game Over
import random
import os
from PIL import Image, ImageTk
import threading
import time

#----Audio----#
sonido_activo = False
try:
    import pygame
    pygame.mixer.init()
    sonido_activo = True
except Exception:
    sonido_activo = False 

#----Rutas de imagenes y sonidos----#
IMGS_DIR = r'C:\Users\Jimen\Desktop\TEC\Segundo Semestre\Intro 2\proyecto intro\intro\imagenes'
SOUNDS_DIR = os.path.join(os.path.dirname(IMGS_DIR), 'sonidos')

#----imagenes y direcciones de la moto----#
DIRECCIONES = ("derecha", "izquierda", "arriba", "abajo")
COLORES = ("azul", "rosa", "verde")
FRAMES = (1, 2, 3)

#----Tamaños de las imagenes y velocidad de la moto----#
TAMAÑO_SPRITE  = 64
VISTA_PREVIA = 96
VELOCIDAD    = 8

#----Inicia en azul por defecto----#
apariencia_actual = "azul"


#----Color y tamaño de la estela----#
COLOR_ESTELA = "#00FFFF"  # Color para la estela (puedes cambiarlo)
ESTELA_SIZE = 10  # Tamaño de la estela

#----Cache de imagenes y enemigos----#
IMG_CACHE = {}
ENEMIGOS = {}

#----Música de fondo----#
GAME_MUSIC = os.path.join(SOUNDS_DIR, "juego_musica.mp3")

#----Variables globales----#
musica_activada = True
juego_activo = True
programa_activo = True
puntaje = 0
tiempo_transcurrido = 0
PUNTAJES_GUARDADOS = "puntajes.txt"
juego_abierto = False
ventana_secundaria_abierta = None

############################################################################################################################################################################

############################################################## Funciones de la musica y para cargar recursos ###############################################################

#-----Función para el loop de la música de fondo----#
def repetir_musica():
    if not sonido_activo or not programa_activo:
        return

    if musica_activada:
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(GAME_MUSIC)
                pygame.mixer.music.play(-1)
        except:
            pass

    threading.Timer(1, repetir_musica).start()

#-----Función para obtener imagenes con cache----#
def obtener_imagen(nombre, w, h):
    clave = (nombre, w, h)
    if clave in IMG_CACHE:
        return IMG_CACHE[clave]
    ruta = os.path.join(IMGS_DIR, nombre)
    img = Image.open(ruta).resize((w, h), Image.Resampling.LANCZOS)
    ph = ImageTk.PhotoImage(img)
    IMG_CACHE[clave] = ph
    return ph

#-----Función para precargar imagenes----#
def precargar_imagenes(ancho_fondo, alto_fondo, i=0, j=0, k=0):
    global ENEMIGOS

    if i == 0 and j == 0 and k == 0:
        obtener_imagen("fondo_juego.png", ancho_fondo, alto_fondo)

    if i >= len(COLORES):
        precargar_enemigos()
        return

    color = COLORES[i]
    direccion = DIRECCIONES[j]
    frame = FRAMES[k]

    obtener_imagen(f"{color}_{direccion}{frame}.png", TAMAÑO_SPRITE, TAMAÑO_SPRITE)

    if direccion == "derecha" and frame == 1:
        obtener_imagen(f"{color}_derecha1.png", VISTA_PREVIA, VISTA_PREVIA)

    if k + 1 < len(FRAMES):
        precargar_imagenes(ancho_fondo, alto_fondo, i, j, k + 1)
    elif j + 1 < len(DIRECCIONES):
        precargar_imagenes(ancho_fondo, alto_fondo, i, j + 1, 0)
    else:
        precargar_imagenes(ancho_fondo, alto_fondo, i + 1, 0, 0)

#-----Función para precargar imagenes de enemigos----#
def precargar_enemigos(j=0, k=0):
    global ENEMIGOS

    # Inicialización recursiva del diccionario por primera vez
    if j == 0 and k == 0:
        ENEMIGOS = {}
        init_dict_rec(0)

    if j >= len(DIRECCIONES):
        return

    direccion = DIRECCIONES[j]
    frame = FRAMES[k]

    ENEMIGOS[direccion].append(
        obtener_imagen(f"patrulla_{direccion}{frame}.png", TAMAÑO_SPRITE, TAMAÑO_SPRITE)
    )

    if k + 1 < len(FRAMES):
        precargar_enemigos(j, k + 1)
    else:
        precargar_enemigos(j + 1, 0)

#-----Función recursiva para inicializar el diccionario de enemigos----#
def init_dict_rec(i):
    if i >= len(DIRECCIONES):
        return
    ENEMIGOS[DIRECCIONES[i]] = []
    init_dict_rec(i + 1)

#-----Función para cargar imagenes escaladas----#
def Carga_de_Imagenes_Escaladas(nombre, px1, px2):
    return obtener_imagen(nombre, px1, px2)

#----Funciones para guardar y cargar puntajes----#
def cargar_mejores_puntajes():
    if not os.path.exists(PUNTAJES_GUARDADOS):
        return []

    with open(PUNTAJES_GUARDADOS, "r") as f:
        lineas = f.readlines()
        return convertir_lineas_a_int(lineas)

#----Función recursiva para convertir líneas a enteros----#
def convertir_lineas_a_int(lineas, i=0, resultado=None):
    if resultado is None:
        resultado = []
    if i >= len(lineas):
        return resultado
    resultado.append(int(lineas[i].strip()))
    return convertir_lineas_a_int(lineas, i + 1, resultado)

#----Función para guardar los mejores puntajes----#
def guardar_mejores_puntajes(puntaje):
    puntajes = cargar_mejores_puntajes()
    puntajes.append(puntaje)

    puntajes = ordenar_desc(puntajes) 
    puntajes = puntajes[:3] 

    with open(PUNTAJES_GUARDADOS, "w") as f:
        escribir_puntajes(f, puntajes)

#----Función recursiva para ordenar de mayor a menor----#
def ordenar_desc(lista):
    if len(lista) <= 1:
        return lista
    # Tomar el primer elemento, ordenar el resto, luego insertar
    return insertar_en_orden(lista[0], ordenar_desc(lista[1:]))

#----Función recursiva para insertar en orden -----#
def insertar_en_orden(valor, lista, i=0):
    if i >= len(lista):
        return lista + [valor]
    if valor >= lista[i]:
        return lista[:i] + [valor] + lista[i:]
    return insertar_en_orden(valor, lista, i + 1)

#----Función recursiva para escribir puntajes en archivo----#
def escribir_puntajes(f, lista, i=0):
    if i >= len(lista):
        return
    f.write(str(lista[i]) + "\n")
    escribir_puntajes(f, lista, i + 1)

############################################################################################################################################################################
############################################################################ Ventanas y manejo  ############################################################################

#----Manejo de ventanas secundarias----#
def abrir_ventana_secundaria(creador):
    global ventana_secundaria_abierta

    if ventana_secundaria_abierta is not None:
        return  # Ya hay una ventana abierta

    ventana_principal.withdraw()

    ventana = creador()
    ventana_secundaria_abierta = ventana

    def cerrar_controlado():
        volver_al_menu_principal()
    ventana.protocol("WM_DELETE_WINDOW", cerrar_controlado)
    ventana.bind("<<CerrarControlado>>", lambda e: cerrar_controlado())
    return ventana

#----Función para volver al menú principal desde otras ventanas----#
def volver_al_menu_principal():
    global ventana_secundaria_abierta, juego_abierto, juego_activo
    juego_activo = True
    juego_abierto = False

    if ventana_secundaria_abierta is not None:
        try:
            ventana_secundaria_abierta.destroy() 
        except:
            pass
        ventana_secundaria_abierta = None

    ventana_principal.deiconify()


#----Ventana de apariencia y configuración----#
def ventana_apariencia():
    global apariencia_actual
    ventana_apariencia = tk.Toplevel()
    ventana_apariencia.title("Configuración")

    ancho_ventana = ventana_apariencia.winfo_screenwidth()
    alto_ventana = ventana_apariencia.winfo_screenheight()
    ventana_apariencia.geometry(f"{ancho_ventana}x{alto_ventana}")

    imagen = obtener_imagen("fondo_juego.png", ancho_ventana, alto_ventana)
    Imagen_fondo_juego = Label(ventana_apariencia, image=imagen)
    Imagen_fondo_juego.place(x=0, y=0, relwidth=1, relheight=1)
    ventana_apariencia.imagen_fondo = imagen

    ventana_apariencia.preview_azul  = obtener_imagen("azul_derecha1.png", VISTA_PREVIA, VISTA_PREVIA)
    ventana_apariencia.preview_rosa  = obtener_imagen("rosa_derecha1.png", VISTA_PREVIA, VISTA_PREVIA)
    ventana_apariencia.preview_verde = obtener_imagen("verde_derecha1.png", VISTA_PREVIA, VISTA_PREVIA)

    var_apariencia = tk.StringVar(value=apariencia_actual)

    marco = Frame(ventana_apariencia, bg="#000000")
    marco.place(relx=0.5, rely=0.5, anchor="center")

    Label(marco, text="Configuración", font=("Arial", 22, "bold"),
          fg="white", bg="#000000").pack(pady=(10, 18))

    Label(marco, text="Apariencia de la motocicleta",
          font=("Arial", 16, "bold"), fg="white", bg="#000000").pack()
    
    #----Activar o desactivar música----#
    estado_musica = tk.BooleanVar(value=pygame.mixer.music.get_busy() if sonido_activo else False)

    def toggle_musica():
        global musica_activada
        if not sonido_activo:
            return

        if estado_musica.get():
            musica_activada = True
            pygame.mixer.music.unpause()
        else:
            musica_activada = False
            pygame.mixer.music.pause()


    Checkbutton(marco, text="Activar música",
                variable=estado_musica, command=toggle_musica,
                font=("Arial", 14), bg="#000000", fg="white",
                activebackground="#333333",
                selectcolor="#444444").pack(pady=10)
    
     #-----Función para cambiar volumen----#
    def cambiar_volumen(val):
        if sonido_activo:
            pygame.mixer.music.set_volume(float
                                          (val) / 100)
            
    vol_actual = pygame.mixer.music.get_volume() * 100 if sonido_activo else 70
    Label(marco, text="Volumen de la música",
        font=("Arial", 14, "bold"), fg="white", bg="#000000").pack()

    slider_vol = Scale(marco, from_=0, to=100, orient="horizontal",
                    command=cambiar_volumen,
                    length=260, bg="#111111", fg="white",
                    troughcolor="#444444", highlightthickness=0)
    slider_vol.set(vol_actual)
    slider_vol.pack(pady=5)

    #----Opciones para cambiar apariencia----#
    opciones = Frame(marco, bg="#000000")
    opciones.pack(pady=10)

    valores = ("azul", "rosa", "verde")
    imagenes = (
        ventana_apariencia.preview_azul,
        ventana_apariencia.preview_rosa,
        ventana_apariencia.preview_verde
    )

    def crear_radios(i=0):
        if i >= len(valores):
            return
        val = valores[i]
        img = imagenes[i]

        Radiobutton(
            opciones, text=val.capitalize(), variable=var_apariencia,
            value=val, image=img, compound="top",
            indicatoron=False, width=VISTA_PREVIA + 40,
            height=VISTA_PREVIA + 44, font=("Arial", 12, "bold"),
            fg="white", bg="#222222", selectcolor="#444444",
            activebackground="#333333"
        ).pack(side="left", padx=15)

        crear_radios(i + 1)

    crear_radios() 

    def guardar_apariencia():
        global apariencia_actual
        apariencia_actual = var_apariencia.get()
        volver_al_menu_principal()

    Button(marco, text="Guardar",
        command=guardar_apariencia,
        font=("Arial", 14, "bold"),
        bg="#5A9DB2", fg="black",
        width=16, height=1).pack(pady=15)

    return ventana_apariencia


#----Crea la ventana del salón de la fama con los puntajes----#
def salon_de_la_fama():
    top = tk.Toplevel()
    top.title("Salón de la Fama")

    ancho_ventana = top.winfo_screenwidth()
    alto_ventana = top.winfo_screenheight()
    top.geometry(f"{ancho_ventana}x{alto_ventana}")

    # Fondo del salón
    imagen = obtener_imagen("fondo_juego.png", ancho_ventana, alto_ventana)
    Label(top, image=imagen).place(x=0, y=0, relwidth=1, relheight=1)
    top.imagen_fondo = imagen

    # Marco central
    marco = Frame(top, bg="#000000")
    marco.place(relx=0.5, rely=0.5, anchor="center")

    Label(marco, text="🏆 SALÓN DE LA FAMA 🏆",
          font=("Arial", 26, "bold"),
          fg="yellow", bg="#000000").pack(pady=(10,20))

    puntajes = cargar_mejores_puntajes()

    if puntajes:
        mostrar_puntajes_rec(marco, puntajes, 0)
    else:
        Label(marco, text="Aún no hay puntajes guardados",
              font=("Arial", 18),
              fg="white", bg="#000000").pack(pady=10)

    Button(marco, text="Cerrar",
        font=("Arial", 14, "bold"),
        width=14, bg="#5A9DB2", fg="black",
        command=volver_al_menu_principal).pack(pady=20)
    return top

#----Función recursiva para mostrar puntajes en salon de la fama----#
def mostrar_puntajes_rec(marco, puntajes, i):
    if i >= len(puntajes):
        return

    Label(marco, text=f"{i+1}. {puntajes[i]} puntos",
          font=("Arial", 18, "bold"),
          fg="white", bg="#000000").pack(pady=5)

    mostrar_puntajes_rec(marco, puntajes, i + 1)

############################################################################################################################################################################
################################################################### Funcionalidad del jugador ##############################################################################

#----Funcion para mover el jugador según la tecla presionada----#
def mover_jugador(can, event, velocidad, ancho_can, alto_can):
    key = (event.keysym or "").lower()
    if key == 'a':
        can.ultima_direccion = "izquierda"
    elif key == 'd':
        can.ultima_direccion = "derecha"
    elif key == 'w':
        can.ultima_direccion = "arriba"
    elif key == 's':
        can.ultima_direccion = "abajo"
    can.moviendo = True

#----Funcion para el movimiento continuo del jugador----#
def mover_jugador_continuo(can, velocidad, ancho_can, alto_can):
    if not juego_activo:
        return
    if getattr(can, "moviendo", False):
        dx = dy = 0
        if can.ultima_direccion == "izquierda":
            dx = -velocidad
        elif can.ultima_direccion == "derecha":
            dx = velocidad
        elif can.ultima_direccion == "arriba":
            dy = -velocidad
        elif can.ultima_direccion == "abajo":
            dy = velocidad

        can.move(can.jugador, dx, dy)
        fuera_pantalla(can, can.jugador, ancho_can, alto_can)

        nuevo_set = can.sprites_por_dir.get(can.ultima_direccion)
        if nuevo_set is not None:
            if nuevo_set is not can.anim_set_actual:
                can.anim_set_actual = nuevo_set
                can.indice_sprite = 0

            can.indice_sprite = (can.indice_sprite + 1) % len(can.anim_set_actual)
            can.itemconfig(can.jugador, image=can.anim_set_actual[can.indice_sprite])


        #---Establecer color según apariencia del jugador----#
        if apariencia_actual == "azul":
            COLOR_JUGADOR = "#00FFFF"
        elif apariencia_actual == "rosa":
            COLOR_JUGADOR = "#FF69B4"
        elif apariencia_actual == "verde":
            COLOR_JUGADOR = "#32CD32"
        else:
            COLOR_JUGADOR = "#FFFFFF"  # fallback

        #----Crear estela del jugador con color dinámico----#
        x, y = can.coords(can.jugador)
        estela = can.create_oval(
            x - dx - ESTELA_SIZE//2, y - dy - ESTELA_SIZE//2,
            x - dx + ESTELA_SIZE//2, y - dy + ESTELA_SIZE//2,
            fill=COLOR_JUGADOR, outline=COLOR_JUGADOR
        )
        can.estelas.append((estela, "jugador"))

        # ✅ Estela desaparece después de 2000ms (2s)
        can.after(2000, borrar_estela, can, estela)

    # Llamar nuevamente para asegurar que el movimiento continúe
    can.after(20, mover_jugador_continuo, can, VELOCIDAD, ancho_can, alto_can)

#----Función para crear el personaje del jugador----#
def crear_personaje(can, x, y, moto):
    return can.create_image(x, y, image=moto)

#----Funcion para manejar cuando el objeto sale de la pantalla----#
def fuera_pantalla(can, objeto, ancho, alto):
    x, y = can.coords(objeto)
    bbox = can.bbox(objeto)
    if bbox:
        x1, y1, x2, y2 = bbox
        w = x2 - x1; h = y2 - y1
    else:
        w = h = TAMAÑO_SPRITE

    if x < -w: x = ancho + w
    elif x > ancho + w: x = -w
    if y < -h: y = alto + h
    elif y > alto + h: y = -h

    can.coords(objeto, x, y)

############################################################################################################################################################################
#################################################################### Creacion de las estelas ###############################################################################

#----Función para crear una estela detrás de un objeto----#
def crear_estela(can, objeto, dx, dy, dueño):
    x, y = can.coords(objeto)
    estela = can.create_oval(
        x - dx - ESTELA_SIZE//2, y - dy - ESTELA_SIZE//2,
        x - dx + ESTELA_SIZE//2, y - dy + ESTELA_SIZE//2,
        fill=COLOR_ESTELA, outline=COLOR_ESTELA
    )
    can.estelas.append((estela, dueño))

#----Función para borrar una estela después de cierto tiempo----#
def borrar_estela(can, estela):
    if estela:
        try:
            can.delete(estela)
            can.estelas = filtrar_estelas(can.estelas, estela)
        except:
            pass

#----Función para filtrar estelas----#
def filtrar_estelas(lista, estela):
    if not lista: 
        return []
    
    e, d = lista[0]
    resto = filtrar_estelas(lista[1:], estela)

    return resto if e == estela else [(e, d)] + resto

############################################################################################################################################################################
################################################################# Funcionalidad de enemigos ################################################################################

#----Función para crear un enemigo y deferenciar los 3----#
def crear_enemigo(can, imagen, x, y, velocidad, ancho_canvas, alto_canvas, enemigo_id):
    dir_actual = random.choice(DIRECCIONES)
    if dir_actual == "derecha": vel_x, vel_y = velocidad, 0
    elif dir_actual == "izquierda": vel_x, vel_y = -velocidad, 0
    elif dir_actual == "arriba": vel_x, vel_y = 0, -velocidad
    else: vel_x, vel_y = 0, velocidad

    sprite = crear_personaje(can, x, y, ENEMIGOS[dir_actual][0])

    return [sprite, vel_x, vel_y, dir_actual, 0, velocidad, enemigo_id]

#----Función para cambiar la dirección de un enemigo aleatoriamente----#
def cambiar_direccion_aleatoria(can, enemigo):
    dir_actual, vel = enemigo[3], enemigo[5]

    nueva_dir = random.choice(DIRECCIONES)
    if nueva_dir == "derecha": enemigo[1], enemigo[2] = vel, 0
    elif nueva_dir == "izquierda": enemigo[1], enemigo[2] = -vel, 0
    elif nueva_dir == "arriba": enemigo[1], enemigo[2] = 0, -vel
    elif nueva_dir == "abajo": enemigo[1], enemigo[2] = 0, vel

    enemigo[3] = nueva_dir

#----Función para programar cambio de dirección aleatoria----#
def programar_cambio_dir(can, ventana, enemigo):
    cambiar_direccion_aleatoria(can, enemigo)
    tiempo = random.randint(1500, 3500)
    ventana.after(tiempo, programar_cambio_dir, can, ventana, enemigo)

#----Función recursiva para programar cambios de dirección en todos los enemigos----#
def programar_enemigos(can, ventana, lista, i):
    if i >= len(lista):
        return
    programar_cambio_dir(can, ventana, lista[i])
    programar_enemigos(can, ventana, lista, i + 1)

#----Función hacer que el enemigo eliminado vuelva a aparecer----#
def respawnear_enemigo(can, ventana, enemigo_index, ancho_canvas, alto_canvas):
    if not juego_activo:
        return

    x = random.randint(100, ancho_canvas - 100)
    y = random.randint(100, alto_canvas - 100)

    velocidad = random.randint(5, 8)

    nuevo = crear_enemigo(can, None, x, y, velocidad, ancho_canvas, alto_canvas, f"e{enemigo_index}")
    setattr(ventana, f"enemigo{enemigo_index}", nuevo)

    programar_cambio_dir(can, ventana, nuevo)

#----Función para mover un enemigo y crear su estela----#
def mover_un_enemigo(can, enemigo, ancho_canvas, alto_canvas):
    sprite, vel_x, vel_y, dir_actual, frame_idx, velocidad, enemigo_id = enemigo

    can.move(sprite, vel_x, vel_y)
    fuera_pantalla(can, sprite, ancho_canvas, alto_canvas)

    crear_estela(can, sprite, vel_x, vel_y, enemigo[6])

    ultimo = can.estelas[-1][0]
    can.after(2000, borrar_estela, can, ultimo)

    enemigo[4] = (frame_idx + 1) % len(ENEMIGOS[dir_actual])
    can.itemconfig(sprite, image=ENEMIGOS[dir_actual][enemigo[4]])

    return enemigo

#----Función para mover todos los enemigos vivos----#
def mover_enemigos_vivos(can, enemigos, ancho, alto, i=0):
    if i >= len(enemigos):
        return
    e = enemigos[i]
    if e[0] is not None:
        mover_un_enemigo(can, e, ancho, alto)
    mover_enemigos_vivos(can, enemigos, ancho, alto, i + 1)

############################################################################################################################################################################
################################################################# Funciones de las colisiones ##############################################################################

#----Función para detectar colisión entre un objeto y las estelas----#
def colision_con_estela(can, objeto, dueño_objeto, i=0):
    p_objeto = can.bbox(objeto)
    if not p_objeto:
        return False

    if i >= len(can.estelas):
        return False

    estela, dueño_estela = can.estelas[i]

    # Ignorar la estela del mismo dueño
    if dueño_objeto != dueño_estela:
        p_estela = can.bbox(estela)
        if p_estela and (
            p_objeto[0] < p_estela[2] and p_objeto[2] > p_estela[0] and
            p_objeto[1] < p_estela[3] and p_objeto[3] > p_estela[1]
        ):
            return True

    return colision_con_estela(can, objeto, dueño_objeto, i + 1)

#----Función para manejar colisión entre dos enemigos----#
def colision_entre_dos(can, enemigo1, enemigo2):
    p1 = can.bbox(enemigo1[0])
    p2 = can.bbox(enemigo2[0])
    if p1 and p2:
        if (p1[0] < p2[2] and p1[2] > p2[0] and
            p1[1] < p2[3] and p1[3] > p2[1]):

            cambiar_direccion_aleatoria(can, enemigo1)
            cambiar_direccion_aleatoria(can, enemigo2)

            can.move(enemigo1[0], enemigo1[1] * 3, enemigo1[2] * 3)
            can.move(enemigo2[0], enemigo2[1] * 3, enemigo2[2] * 3)

#----Función para detectar colisión entre enemigo y jugador----#
def colision_enemigo_con_jugador(can, enemigo, jugador):
    p1 = can.bbox(enemigo[0])
    p2 = can.bbox(jugador)
    if p1 and p2:
        return (p1[0] < p2[2] and p1[2] > p2[0] and
                p1[1] < p2[3] and p1[3] > p2[1])
    return False

#----Función para filtrar enemigos vivos----#
def filtrar_vivos(enemigos, i=0, resultado=None):
    if resultado is None:
        resultado = []
    if i >= len(enemigos):
        return resultado
    if enemigos[i][0] is not None:
        resultado.append(enemigos[i])
    return filtrar_vivos(enemigos, i + 1, resultado)

#----Función para manejar colisiones entre enemigos vivos----#
def colisiones_entre_enemigos(can, vivos, i, j):
    if i >= len(vivos):
        return
    if j >= len(vivos):
        colisiones_entre_enemigos(can, vivos, i + 1, i + 2)
        return

    colision_entre_dos(can, vivos[i], vivos[j])
    colisiones_entre_enemigos(can, vivos, i, j + 1)

#----Función para verificar colisiones de enemigos con estelas y eliminarlos----#
def verificar_estelas_y_eliminar(can, ventana, enemigos, ancho, alto, i=0):
    if i >= len(enemigos):
        return

    e = enemigos[i]
    if e[0] is not None and colision_con_estela(can, e[0], e[6]):
        idx = i + 1
        can.delete(e[0])
        e[0] = None
        ventana.after(2500, respawnear_enemigo,
                      can, ventana, idx, ancho, alto)

    verificar_estelas_y_eliminar(can, ventana, enemigos, ancho, alto, i + 1)

############################################################################################################################################################################
############################################################ animacion de enemigos y registro de puntaje y tiempo ##########################################################

#----Función principal para animar los tres enemigos----#
def animar_tres_enemigos(can, ventana, ancho_canvas, alto_canvas):
    try:
        if not juego_activo:
            return

        enemigos = [ventana.enemigo1, ventana.enemigo2, ventana.enemigo3]

        mover_enemigos_vivos(can, enemigos, ancho_canvas, alto_canvas)

        verificar_estelas_y_eliminar(can, ventana, enemigos, ancho_canvas, alto_canvas)

        if colision_con_estela(can, can.jugador, "jugador"):
            game_over(ventana)
            return

        vivos = filtrar_vivos(enemigos)
        colisiones_entre_enemigos(can, vivos, 0, 1)

        ventana.after(20, animar_tres_enemigos, can, ventana, ancho_canvas, alto_canvas)

    except Exception as ex:
        print("ERROR animar_tres_enemigos:", ex)

#----Función para actualizar tiempo y puntos cada segundo----#
def actualizar_tiempo_y_puntos(ventana):
    global tiempo_transcurrido, puntaje, juego_activo
    
    if not juego_activo:
        return

    tiempo_transcurrido += 1

    if tiempo_transcurrido % 10 == 0:
        puntaje += 100

    ventana.marcador.config(
        text=f"Tiempo: {tiempo_transcurrido}s | Puntos: {puntaje}"
    )

    ventana.after(1000, actualizar_tiempo_y_puntos, ventana)

############################################################################################################################################################################
############################################################################ Ventana Game Over #############################################################################

#----Función para mostrar la ventana de Game Over el tiempo que tardó y el puntaje obtenido----#
def game_over(ventana_juego):
    global juego_activo, tiempo_transcurrido, puntaje
    juego_activo = False

    if sonido_activo:
        pygame.mixer.music.pause()

    guardar_mejores_puntajes(puntaje)

    go = tk.Toplevel()
    go.title("Game Over")
    ancho_go = 600
    alto_go = 300

    ancho_pantalla = go.winfo_screenwidth()
    alto_pantalla = go.winfo_screenheight()

    x = (ancho_pantalla // 2) - (ancho_go // 2)
    y = (alto_pantalla // 2) - (alto_go // 2)

    go.geometry(f"{ancho_go}x{alto_go}+{x}+{y}")

    go.config(bg="#000000")
    go.grab_set() 

    Label(go, text="GAME OVER", font=("Arial", 26, "bold"),
          fg="red", bg="#000000").pack(pady=10)

    Label(go, text="¡Has sido atrapado!",
          font=("Arial", 16), fg="white", bg="#000000").pack(pady=10)

    Label(go, text=f"Tiempo sobrevivido: {tiempo_transcurrido} s",
      font=("Arial", 14), fg="white", bg="#000000").pack(pady=5)

    Label(go, text=f"Puntuación final: {puntaje}",
      font=("Arial", 16, "bold"), fg="yellow", bg="#000000").pack(pady=5)

    def reiniciar():
        global juego_activo, juego_abierto
        juego_activo = True
        juego_abierto = False  
        go.destroy()
        ventana_juego.destroy() 
        juego()  

    def volver_menu():
        global juego_activo, juego_abierto, ventana_secundaria_abierta
        juego_activo = True  
        juego_abierto = False
        ventana_secundaria_abierta = None

        go.destroy()
        try:
            ventana_juego.destroy()
        except:
            pass
        ventana_principal.deiconify()

        if sonido_activo:
            pygame.mixer.music.unpause()


    Button(go, text="Reiniciar", font=("Arial", 14, "bold"),
           width=14, bg="#5A9DB2", fg="black",
           command=reiniciar).pack(pady=10)

    Button(go, text="Menú Principal", font=("Arial", 14, "bold"),
           width=14, bg="#B25A5A", fg="black",
           command=volver_menu).pack(pady=5)

############################################################################################################################################################################
##################################################################### Funcionalidad principal del juego ####################################################################

#----Función para crear el estilo del fondo tipo Tron----#
def crear_grid_tron(canvas, width, height, spacing=40, x=0, y=0, fase=0):
    if fase == 0: 
        if x >= width:
            return crear_grid_tron(canvas, width, height, spacing, 0, 0, 1)
        canvas.create_line(x, 0, x, height, fill="#0A2847", width=2)
        return crear_grid_tron(canvas, width, height, spacing, x + spacing, 0, 0)

    elif fase == 1:
        if y >= height:
            return crear_grid_tron(canvas, width, height, spacing, 0, 0, 2)
        canvas.create_line(0, y, width, y, fill="#0A2847", width=2)
        return crear_grid_tron(canvas, width, height, spacing, 0, y + spacing, 1)

    elif fase == 2:  
        canvas.create_rectangle(0, 0, width, height, outline="#00FFFF", width=4)
        return

#----Función recursiva para cargar los sprites del jugador----#
def cargar_sprites_jugador(sprites, ci, di, fi):
    if ci >= len(COLORES):
        return
    color = COLORES[ci]
    d = DIRECCIONES[di]
    f = FRAMES[fi]

    name = f"{color}_{d}{f}.png"
    sprites[(color, d, f)] = obtener_imagen(name, TAMAÑO_SPRITE, TAMAÑO_SPRITE)

    if fi + 1 < len(FRAMES):
        return cargar_sprites_jugador(sprites, ci, di, fi+1)
    elif di + 1 < len(DIRECCIONES):
        return cargar_sprites_jugador(sprites, ci, di+1, 0)
    else:
        return cargar_sprites_jugador(sprites, ci+1, 0, 0)
    
#----Función recursiva para obtener los frames de una dirección específica----#
def obtener_frames(sprites, color, d, j, lista):
    if j >= len(FRAMES):
        return lista
    lista.append(sprites[(color, d, FRAMES[j])])
    return obtener_frames(sprites, color, d, j + 1, lista)

#----Funcion que crea un diccionario con los sprites por dirección----#
def crear_diccionario_sprites(sprites, color, i, dic):
    if i >= len(DIRECCIONES):
        return dic
    d = DIRECCIONES[i]
    dic[d] = obtener_frames(sprites, color, d, 0, [])
    return crear_diccionario_sprites(sprites, color, i + 1, dic)

#----Crea la ventana donde se va ejecutar el juego----#
def juego():
    global juego_activo, puntaje, tiempo_transcurrido, juego_abierto, ventana_secundaria_abierta
    if juego_abierto:
        return
    juego_abierto = True
    juego_activo = True
    puntaje = 0
    tiempo_transcurrido = 0

    ventana_juego = tk.Toplevel()
    ventana_juego.title("Juego")
    ventana_secundaria_abierta = ventana_juego

    ancho_ventana = ventana_juego.winfo_screenwidth()
    alto_ventana = ventana_juego.winfo_screenheight()
    ventana_juego.geometry(f"{ancho_ventana}x{alto_ventana}")

    imagen = obtener_imagen("fondo_juego.png", ancho_ventana, alto_ventana)
    Label(ventana_juego, image=imagen).place(x=0, y=0, relwidth=1, relheight=1)
    ventana_juego.imagen_fondo = imagen

    marcador = Label(ventana_juego, text="Tiempo: 0s | Puntos: 0",
                     font=("Arial", 16, "bold"), bg="black", fg="white")
    marcador.pack()
    ventana_juego.marcador = marcador

    ancho_canvas = int(ancho_ventana * 0.8) // TAMAÑO_SPRITE * TAMAÑO_SPRITE
    alto_canvas  = int(alto_ventana * 0.8)  // TAMAÑO_SPRITE * TAMAÑO_SPRITE
    canvas_juego = Canvas(ventana_juego, width=ancho_canvas, height=alto_canvas, bg="black")
    canvas_juego.pack()
    canvas_juego.estelas = []

    crear_grid_tron(canvas_juego, ancho_canvas, alto_canvas)

    sprites = {}
    cargar_sprites_jugador(sprites, 0, 0, 0)

    actualizar_tiempo_y_puntos(ventana_juego)

    dic = crear_diccionario_sprites(sprites, apariencia_actual, 0, {})
    canvas_juego.sprites_por_dir = dic
    canvas_juego.anim_set_actual = dic["arriba"]
    canvas_juego.indice_sprite = 0

    canvas_juego.jugador = crear_personaje(
        canvas_juego, ancho_canvas//2, alto_canvas//2, canvas_juego.anim_set_actual[0]
    )
    canvas_juego.ultima_direccion = "arriba"
    canvas_juego.moviendo = True

    ventana_juego.focus_force()
    canvas_juego.focus_force()

    ventana_juego.bind_all("<KeyPress>",
        lambda e: mover_jugador(canvas_juego, e, VELOCIDAD, ancho_canvas, alto_canvas))

    ventana_juego.enemigo1 = crear_enemigo(canvas_juego, None, 200, 150, 7, ancho_canvas, alto_canvas, "e1")
    ventana_juego.enemigo2 = crear_enemigo(canvas_juego, None, 800, 300, 8, ancho_canvas, alto_canvas, "e2")
    ventana_juego.enemigo3 = crear_enemigo(canvas_juego, None, 500, 450, 9, ancho_canvas, alto_canvas, "e3")


    programar_enemigos(canvas_juego, ventana_juego, [ventana_juego.enemigo1,
                                                     ventana_juego.enemigo2,
                                                     ventana_juego.enemigo3], 0)

    animar_tres_enemigos(canvas_juego, ventana_juego, ancho_canvas, alto_canvas)
    mover_jugador_continuo(canvas_juego, VELOCIDAD, ancho_canvas, alto_canvas)
    return ventana_juego

############################################################################################################################################################################
############################################################################ Ventana principal #############################################################################


ventana_principal = tk.Tk()
ventana_principal.title("Taller tkinter")

ancho_ventana = ventana_principal.winfo_screenwidth()
alto_ventana = ventana_principal.winfo_screenheight()
ventana_principal.geometry(f"{ancho_ventana}x{alto_ventana}")

precargar_imagenes(ancho_ventana, alto_ventana)

imagen = obtener_imagen("fondo_juego.png", ancho_ventana, alto_ventana)
Label(ventana_principal, image=imagen).place(x=0, y=0)
ventana_principal.imagen_fondo = imagen

repetir_musica()

Button(ventana_principal, text="Jugar", font=("arial", 15),
       command=lambda: abrir_ventana_secundaria(juego),
       width=40, height=2, bg="#5A9DB2", fg="black").place(x=550, y=400)

Button(ventana_principal, text="Configuración", font=("arial", 10),
       command=lambda: abrir_ventana_secundaria(ventana_apariencia),
       width=20, height=2, bg="#5A9DB2", fg="black").place(x=50, y=50)

Button(ventana_principal, text="Salón de la Fama", font=("arial", 10),
       command=lambda: abrir_ventana_secundaria(salon_de_la_fama),
       width=20, height=2, bg="#5A9DB2", fg="black").place(x=1320, y=50)

def detener_musica_y_salir():
    global programa_activo  
    programa_activo = False
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    ventana_principal.destroy()

ventana_principal.protocol("WM_DELETE_WINDOW", detener_musica_y_salir)

ventana_principal.mainloop()