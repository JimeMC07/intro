import tkinter as tk
from tkinter import *
import random
import os
from PIL import Image, ImageTk
import threading
import time

# ==== AUDIO SOLO MUSICA DE JUEGO EN HILO ====
AUDIO_OK = False
try:
    import pygame
    pygame.mixer.init()
    AUDIO_OK = True
except Exception:
    AUDIO_OK = False  # silencioso si no hay audio

# ===== Config y estado =====
IMGS_DIR = r'C:\Users\Jimen\Desktop\TEC\Segundo Semestre\Intro 2\proyecto intro\intro\imagenes'
SOUNDS_DIR = os.path.join(os.path.dirname(IMGS_DIR), 'sonidos')
DIRECCIONES = ("derecha", "izquierda", "arriba", "abajo")
COLORES = ("azul", "rosa", "verde")
FRAMES = (1, 2, 3)

# ==== TAMAÑOS ====
SPRITE_SIZE  = 64
PREVIEW_SIZE = 96
VELOCIDAD    = max(10, SPRITE_SIZE // 2)

apariencia_actual = "azul"

# ===== Cachés =====
IMG_CACHE = {}
ENEMIGOS = {}

# ✅ Flags para manejo de ventanas
juego_abierto = False
config_abierta = False
puntajes_abiertos = False  # ✅ nuevo flag

# ✅ ===== SISTEMA DE PUNTAJES =====
ARCHIVO_PUNTAJES = "puntajes.txt"

def cargar_puntajes():
    if not os.path.exists(ARCHIVO_PUNTAJES):
        return []
    try:
        with open(ARCHIVO_PUNTAJES, "r") as f:
            puntajes = [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]
        return sorted(puntajes, reverse=True)[:3]
    except:
        return []

def guardar_puntaje(p):
    puntajes = cargar_puntajes()
    puntajes.append(p)
    puntajes = sorted(puntajes, reverse=True)[:3]
    with open(ARCHIVO_PUNTAJES, "w") as f:
        for x in puntajes:
            f.write(str(x)+"\n")

def mostrar_puntajes():
    global puntajes_abiertos
    if puntajes_abiertos:
        return
    puntajes_abiertos = True

    ventana_principal.withdraw()  # ✅ Ocultar menú

    ventana_puntajes = tk.Toplevel()
    ventana_puntajes.title("Mejores Puntajes")

    def cerrar_puntajes():
        global puntajes_abiertos
        puntajes_abiertos = False
        ventana_principal.deiconify()
        ventana_puntajes.destroy()

    ventana_puntajes.protocol("WM_DELETE_WINDOW", cerrar_puntajes)

    # ✅ Pantalla completa como las demás ventanas
    ancho = ventana_puntajes.winfo_screenwidth()
    alto  = ventana_puntajes.winfo_screenheight()
    ventana_puntajes.geometry(f"{ancho}x{alto}")

    # ✅ Colocar EL MISMO FONDO
    fondo = get_img("fondo_juego.png", ancho, alto)
    Label(ventana_puntajes, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    ventana_puntajes.fondo = fondo  # evitar ser recolectado por GC

    # ===== INTERFAZ =====
    marco = Frame(ventana_puntajes, bg="#000000", padx=30, pady=30)
    marco.place(relx=0.5, rely=0.5, anchor="center")

    Label(marco, text="TOP 3 PUNTAJES", font=("Arial", 26, "bold"),
          fg="white", bg="#000000").pack(pady=22)

    puntajes = cargar_puntajes()

    if not puntajes:
        Label(marco, text="No hay puntajes aún", font=("Arial", 18),
              fg="white", bg="#000000").pack(pady=10)
    else:
        for i, p in enumerate(puntajes, start=1):
            Label(marco, text=f"{i}. {p} puntos", font=("Arial", 20, "bold"),
                  fg="#FFD700", bg="#000000").pack(pady=6)

    Button(marco, text="Cerrar", command=cerrar_puntajes, font=("Arial", 14),
           bg="#5A9DB2", fg="black", width=12).pack(pady=18)




# >>>>>> ÚNICA PISTA DE MÚSICA <<<<<<
GAME_MUSIC = os.path.join(SOUNDS_DIR, "juego_musica.mp3")

# =========== CORRECCIÓN SIN WHILE ===========
def music_loop():
    if not AUDIO_OK:
        return
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(GAME_MUSIC)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
    except:
        return
    
    threading.Timer(1, music_loop).start()  # Recursión programada

# ===== Imagen =====
def get_img(nombre, w, h):
    clave = (nombre, w, h)
    if clave in IMG_CACHE:
        return IMG_CACHE[clave]
    ruta = os.path.join(IMGS_DIR, nombre)
    img = Image.open(ruta).resize((w, h), Image.Resampling.LANCZOS)
    ph = ImageTk.PhotoImage(img)
    IMG_CACHE[clave] = ph
    return ph

# =========== CORRECCIÓN SIN FOR ===========
def precargar_imagenes(ancho_fondo, alto_fondo, i=0, j=0, k=0):
    global ENEMIGOS

    if i == 0 and j == 0 and k == 0:
        get_img("fondo_juego.png", ancho_fondo, alto_fondo)

    if i >= len(COLORES):
        precargar_enemigos()
        return

    color = COLORES[i]
    direccion = DIRECCIONES[j]
    frame = FRAMES[k]

    get_img(f"{color}_{direccion}{frame}.png", SPRITE_SIZE, SPRITE_SIZE)

    if direccion == "derecha" and frame == 1:
        get_img(f"{color}_derecha1.png", PREVIEW_SIZE, PREVIEW_SIZE)

    if k + 1 < len(FRAMES):
        precargar_imagenes(ancho_fondo, alto_fondo, i, j, k + 1)
    elif j + 1 < len(DIRECCIONES):
        precargar_imagenes(ancho_fondo, alto_fondo, i, j + 1, 0)
    else:
        precargar_imagenes(ancho_fondo, alto_fondo, i + 1, 0, 0)

def precargar_enemigos(j=0, k=0):
    global ENEMIGOS

    if j == 0 and k == 0:
        ENEMIGOS = {
            "derecha": [],
            "izquierda": [],
            "arriba": [],
            "abajo": []
        }

    if j >= len(DIRECCIONES):
        return

    direccion = DIRECCIONES[j]
    frame = FRAMES[k]

    ENEMIGOS[direccion].append(
        get_img(f"patrulla_{direccion}{frame}.png", SPRITE_SIZE, SPRITE_SIZE)
    )

    if k + 1 < len(FRAMES):
        precargar_enemigos(j, k + 1)
    else:
        precargar_enemigos(j + 1, 0)

def Carga_de_Imagenes_Escaladas(nombre, px1, px2):
    return get_img(nombre, px1, px2)

def juego():
    global juego_abierto
    if juego_abierto:
        return
    juego_abierto = True

    ventana_principal.withdraw()

    ventana_juego = tk.Toplevel()
    ventana_juego.title("Juego")

    def cerrar_juego():
        global juego_abierto
        juego_abierto = False
        ventana_principal.deiconify()
        ventana_juego.destroy()

    ventana_juego.protocol("WM_DELETE_WINDOW", cerrar_juego)

    ancho_ventana = ventana_juego.winfo_screenwidth()
    alto_ventana = ventana_juego.winfo_screenheight()
    ventana_juego.geometry(f"{ancho_ventana}x{alto_ventana}")

    imagen = get_img("fondo_juego.png", ancho_ventana, alto_ventana)
    Imagen_fondo_juego = Label(ventana_juego, image=imagen)
    Imagen_fondo_juego.place(x=0, y=0, relwidth=1, relheight=1)
    ventana_juego.imagen_fondo = imagen

    ancho_canvas = int(ancho_ventana * 0.8) // SPRITE_SIZE * SPRITE_SIZE
    alto_canvas  = int(alto_ventana * 0.8)  // SPRITE_SIZE * SPRITE_SIZE
    canvas_juego = Canvas(ventana_juego, width=ancho_canvas, height=alto_canvas, bg="black")
    canvas_juego.pack()

    # ========= Carga sprites =========
    rosa_derecha1 = get_img("rosa_derecha1.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa1 = rosa_derecha1
    rosa_derecha2 = get_img("rosa_derecha2.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa2 = rosa_derecha2
    rosa_derecha3 = get_img("rosa_derecha3.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa3 = rosa_derecha3
    rosa_arriba1  = get_img("rosa_arriba1.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_up1 = rosa_arriba1
    rosa_arriba2  = get_img("rosa_arriba2.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_up2 = rosa_arriba2
    rosa_arriba3  = get_img("rosa_arriba3.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_up3 = rosa_arriba3
    rosa_abajo1   = get_img("rosa_abajo1.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_down1 = rosa_abajo1
    rosa_abajo2   = get_img("rosa_abajo2.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_down2 = rosa_abajo2
    rosa_abajo3   = get_img("rosa_abajo3.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_down3 = rosa_abajo3
    rosa_izquierda1 = get_img("rosa_izquierda1.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_left1 = rosa_izquierda1
    rosa_izquierda2 = get_img("rosa_izquierda2.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_left2 = rosa_izquierda2
    rosa_izquierda3 = get_img("rosa_izquierda3.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_rosa_left3 = rosa_izquierda3

    azul_derecha1 = get_img("azul_derecha1.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul1 = azul_derecha1
    azul_derecha2 = get_img("azul_derecha2.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul2 = azul_derecha2
    azul_derecha3 = get_img("azul_derecha3.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul3 = azul_derecha3
    azul_arriba1  = get_img("azul_arriba1.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_up1 = azul_arriba1
    azul_arriba2  = get_img("azul_arriba2.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_up2 = azul_arriba2
    azul_arriba3  = get_img("azul_arriba3.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_up3 = azul_arriba3
    azul_abajo1   = get_img("azul_abajo1.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_down1 = azul_abajo1
    azul_abajo2   = get_img("azul_abajo2.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_down2 = azul_abajo2
    azul_abajo3   = get_img("azul_abajo3.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_down3 = azul_abajo3
    azul_izquierda1 = get_img("azul_izquierda1.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_left1 = azul_izquierda1
    azul_izquierda2 = get_img("azul_izquierda2.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_left2 = azul_izquierda2
    azul_izquierda3 = get_img("azul_izquierda3.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_azul_left3 = azul_izquierda3

    verde_derecha1 = get_img("verde_derecha1.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde1 = verde_derecha1
    verde_derecha2 = get_img("verde_derecha2.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde2 = verde_derecha2
    verde_derecha3 = get_img("verde_derecha3.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde3 = verde_derecha3
    verde_arriba1  = get_img("verde_arriba1.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_up1 = verde_arriba1
    verde_arriba2  = get_img("verde_arriba2.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_up2 = verde_arriba2
    verde_arriba3  = get_img("verde_arriba3.png",  SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_up3 = verde_arriba3
    verde_abajo1   = get_img("verde_abajo1.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_down1 = verde_abajo1
    verde_abajo2   = get_img("verde_abajo2.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_down2 = verde_abajo2
    verde_abajo3   = get_img("verde_abajo3.png",   SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_down3 = verde_abajo3
    verde_izquierda1 = get_img("verde_izquierda1.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_left1 = verde_izquierda1
    verde_izquierda2 = get_img("verde_izquierda2.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_left2 = verde_izquierda2
    verde_izquierda3 = get_img("verde_izquierda3.png", SPRITE_SIZE, SPRITE_SIZE); canvas_juego.imagen_verde_left3 = verde_izquierda3

    if apariencia_actual == "rosa":
        set_derecha   = [rosa_derecha1, rosa_derecha2, rosa_derecha3]
        set_izquierda = [rosa_izquierda1, rosa_izquierda2, rosa_izquierda3]
        set_arriba    = [rosa_arriba1,  rosa_arriba2,  rosa_arriba3]
        set_abajo     = [rosa_abajo1,   rosa_abajo2,   rosa_abajo3]
    elif apariencia_actual == "verde":
        set_derecha   = [verde_derecha1, verde_derecha2, verde_derecha3]
        set_izquierda = [verde_izquierda1, verde_izquierda2, verde_izquierda3]
        set_arriba    = [verde_arriba1,  verde_arriba2,  verde_arriba3]
        set_abajo     = [verde_abajo1,   verde_abajo2,   verde_abajo3]
    else:
        set_derecha   = [azul_derecha1, azul_derecha2, azul_derecha3]
        set_izquierda = [azul_izquierda1, azul_izquierda2, azul_izquierda3]
        set_arriba    = [azul_arriba1,  azul_arriba2,  azul_arriba3]
        set_abajo     = [azul_abajo1,   azul_abajo2,   azul_abajo3]

    canvas_juego.sprites_por_dir = {
        "derecha":   set_derecha,
        "izquierda": set_izquierda,
        "arriba":    set_arriba,
        "abajo":     set_abajo
    }
    canvas_juego.anim_set_actual = canvas_juego.sprites_por_dir["arriba"]
    canvas_juego.indice_sprite = 0

    canvas_juego.jugador = crear_personaje(canvas_juego, ancho_canvas//2, alto_canvas//2, canvas_juego.anim_set_actual[0])
    canvas_juego.bind_all("<KeyPress>", lambda event: mover_jugador(canvas_juego, event, VELOCIDAD, ancho_canvas, alto_canvas))
    canvas_juego.ultima_direccion = "arriba"


def ventana_apariencia():
    global config_abierta
    if config_abierta:
        return
    config_abierta = True

    ventana_principal.withdraw()

    ventana_apariencia = tk.Toplevel()
    ventana_apariencia.title("Configuración")

    def cerrar_config():
        global config_abierta
        config_abierta = False
        ventana_principal.deiconify()
        ventana_apariencia.destroy()

    ventana_apariencia.protocol("WM_DELETE_WINDOW", cerrar_config)

    ancho_ventana = ventana_apariencia.winfo_screenwidth()
    alto_ventana = ventana_apariencia.winfo_screenheight()
    ventana_apariencia.geometry(f"{ancho_ventana}x{alto_ventana}")

    imagen = get_img("fondo_juego.png", ancho_ventana, alto_ventana)
    Imagen_fondo_juego = Label(ventana_apariencia, image=imagen)
    Imagen_fondo_juego.place(x=0, y=0, relwidth=1, relheight=1)
    ventana_apariencia.imagen_fondo = imagen

    ventana_apariencia.preview_azul  = get_img("azul_derecha1.png", PREVIEW_SIZE, PREVIEW_SIZE)
    ventana_apariencia.preview_rosa  = get_img("rosa_derecha1.png", PREVIEW_SIZE, PREVIEW_SIZE)
    ventana_apariencia.preview_verde = get_img("verde_derecha1.png", PREVIEW_SIZE, PREVIEW_SIZE)

    global apariencia_actual
    var_apariencia = tk.StringVar(value=apariencia_actual)

    marco = Frame(ventana_apariencia, bg="#000000")
    marco.place(relx=0.5, rely=0.5, anchor="center")

    Label(marco, text="Configuración", font=("Arial", 22, "bold"), fg="white", bg="#000000").pack(pady=(10, 18))

    Label(marco, text="Apariencia de la motocicleta", font=("Arial", 16, "bold"),
          fg="white", bg="#000000").pack()
    opciones = Frame(marco, bg="#000000")
    opciones.pack(pady=10)

    Radiobutton(opciones, text="Azul", variable=var_apariencia, value="azul",
                image=ventana_apariencia.preview_azul, compound="top",
                indicatoron=False, width=PREVIEW_SIZE+40, height=PREVIEW_SIZE+44,
                font=("Arial", 12, "bold"), fg="white",
                bg="#222222", selectcolor="#444444", activebackground="#333333",
                command=lambda: var_apariencia.set("azul")).pack(side="left", padx=15)

    Radiobutton(opciones, text="Rosa", variable=var_apariencia, value="rosa",
                image=ventana_apariencia.preview_rosa, compound="top",
                indicatoron=False, width=PREVIEW_SIZE+40, height=PREVIEW_SIZE+44,
                font=("Arial", 12, "bold"), fg="white",
                bg="#222222", selectcolor="#444444", activebackground="#333333",
                command=lambda: var_apariencia.set("rosa")).pack(side="left", padx=15)

    Radiobutton(opciones, text="Verde", variable=var_apariencia, value="verde",
                image=ventana_apariencia.preview_verde, compound="top",
                indicatoron=False, width=PREVIEW_SIZE+40, height=PREVIEW_SIZE+44,
                font=("Arial", 12, "bold"), fg="white",
                bg="#222222", selectcolor="#444444", activebackground="#333333",
                command=lambda: var_apariencia.set("verde")).pack(side="left", padx=15)

    def guardar_apariencia():
        global apariencia_actual
        apariencia_actual = var_apariencia.get()
        cerrar_config()

    Button(marco, text="Guardar", command=guardar_apariencia,
           font=("Arial", 14), bg="#5A9DB2", fg="black",
           width=12, height=1).pack(pady=12)


# ==== Lógica de juego ====
def crear_personaje(can, x, y, moto):
    return can.create_image(x, y, image=moto)

def mover_jugador(can, event, velocidad, ancho_can, alto_can):
    dx = dy = 0
    if event.keysym == 'a':
        dx = -velocidad; can.ultima_direccion = "izquierda"
    elif event.keysym == 'd':
        dx = velocidad; can.ultima_direccion = "derecha"
    elif event.keysym == 'w':
        dy = -velocidad; can.ultima_direccion = "arriba"
    elif event.keysym == 's':
        dy = velocidad; can.ultima_direccion = "abajo"

    can.move(can.jugador, dx, dy)
    fuera_pantalla(can, can.jugador, ancho_can, alto_can)

    if hasattr(can, 'sprites_por_dir'):
        nuevo_set = can.sprites_por_dir.get(can.ultima_direccion)
        if nuevo_set is not None:
            if nuevo_set is not can.anim_set_actual:
                can.anim_set_actual = nuevo_set
                can.indice_sprite = 0
            if dx != 0 or dy != 0:
                can.indice_sprite = (can.indice_sprite + 1) % len(can.anim_set_actual)
                can.itemconfig(can.jugador, image=can.anim_set_actual[can.indice_sprite])

def fuera_pantalla(can, objeto, ancho, alto):
    x, y = can.coords(objeto)
    bbox = can.bbox(objeto)
    if bbox:
        x1, y1, x2, y2 = bbox
        mitad_ancho = (x2 - x1) / 2
        mitad_alto = (y2 - y1) / 2
    else:
        mitad_ancho = mitad_alto = SPRITE_SIZE // 2

    nx, ny = x, y
    if x + mitad_ancho < 0:      nx = ancho + mitad_ancho
    elif x - mitad_ancho > ancho: nx = -mitad_ancho
    if y + mitad_alto < 0:       ny = alto + mitad_alto
    elif y - mitad_alto > alto:  ny = -mitad_alto
    if nx != x or ny != y:
        can.coords(objeto, nx, ny)

def crear_enemigos(can, nivel):
    x = random.randint(SPRITE_SIZE, 1160)
    y = random.randint(SPRITE_SIZE, 640)
    if nivel == 1:
        imagen = can.imagen_rosa1
    elif nivel == 2:
        imagen = can.imagen_azul1
    elif nivel == 3:
        imagen = can.imagen_verde1
    else:
        return
    can.moto = crear_personaje(can, x, y, imagen)
    return can.moto


# ===== Ventana Principal =====
ventana_principal = tk.Tk()
ventana_principal.title("Taller tkinter")

ancho_ventana = ventana_principal.winfo_screenwidth()
alto_ventana = ventana_principal.winfo_screenheight()
ventana_principal.geometry(f"{ancho_ventana}x{alto_ventana}")

precargar_imagenes(ancho_ventana, alto_ventana)

imagen = get_img("fondo_juego.png", ancho_ventana, alto_ventana)
Imagen_fondo = Label(ventana_principal, image=imagen)
Imagen_fondo.place(x=0, y=0)
ventana_principal.imagen_fondo = imagen

iniciar_hilo_musica = music_loop
iniciar_hilo_musica()

Button(ventana_principal, text="Jugar", font=("arial", 15), command=juego,
       width=40, height=2, bg="#5A9DB2", fg="black").place(x=550, y=200)

Button(ventana_principal, text="Configuración", font=("arial", 10), command=ventana_apariencia,
       width=20, height=2, bg="#5A9DB2", fg="black").place(x=50, y=50)

# ✅ Botón de Puntajes añadido
Button(ventana_principal, text="Puntajes", font=("arial", 10), command=mostrar_puntajes,
       width=20, height=2, bg="#5A9DB2", fg="black").place(x=50, y=120)


def detener_musica_y_salir():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    ventana_principal.destroy()

ventana_principal.protocol("WM_DELETE_WINDOW", detener_musica_y_salir)

ventana_principal.mainloop()
