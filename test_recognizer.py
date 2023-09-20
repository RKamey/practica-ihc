import pygame as pg
import speech_recognition as sr

pg.init()

ancho = 800
alto = 600
ventana = pg.display.set_mode((ancho, alto))
pg.display.set_caption("Mi Ventana Pygame")

# Tamaño de cada casilla del tablero
tam_casilla = 60

def mover_circulo(direccion):
    global pos_x, pos_y

    if direccion == "arriba":
        pos_y -= tam_casilla
    elif direccion == "abajo":
        pos_y += tam_casilla
    elif direccion == "izquierda":
        pos_x -= tam_casilla
    elif direccion == "derecha":
        pos_x += tam_casilla

# Tamaño y grosor del círculo
radio = 30
grosor = 0  # 0 significa un círculo lleno

# Calcular el centro de la ventana
centro_x = ancho // 2
centro_y = alto // 2

# Inicializar posición del círculo en el centro del tablero
pos_x = centro_x
pos_y = centro_y

while True:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            pg.quit()
            quit()

    # Detectar el comando de voz
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Di un comando: arriba, abajo, izquierda o derecha")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio, language="es-ES")
        print(f'Comando reconocido: {command}')
        mover_circulo(command)
    except sr.UnknownValueError:
        print("No se entendió el comando.")
    except sr.RequestError as e:
        print(f"Error en la solicitud: {e}")

    # Limpiar la pantalla
    ventana.fill((255, 255, 255))

    # Dibuja el tablero de 9 casillas centrado
    for i in range(3):
        for j in range(3):
            pg.draw.rect(ventana, (0, 0, 0), (centro_x + (i - 1) * tam_casilla, centro_y + (j - 1) * tam_casilla, tam_casilla, tam_casilla), 2)

    # Dibujar el círculo en la nueva posición
    pg.draw.circle(ventana, (0, 0, 255), (pos_x, pos_y), radio, grosor)

    # Actualizar la pantalla
    pg.display.flip()
