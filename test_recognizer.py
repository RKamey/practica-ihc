# Importamos pygame (para dibujar la ventana) el modelo KaldiRecognizer para
# el reconocimiento de voz y pyaudio para la configuración del micrófono
import pygame as pg
from vosk import Model, KaldiRecognizer
import pyaudio

# Definimos el modelo para el reconocimiento de voz en español
model = Model(r"C:\Users\alons\Downloads\vosk-model-small-es-0.42\vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

# Configuramos el audio del micrófono
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Configuración de pygame
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
    
    try:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            command = (recognizer.Result()[14:-3]).lower()

            if command == "arriba":
                mover_circulo("arriba")
            elif command == "abajo":
                mover_circulo("abajo")
            elif command == "izquierda":
                mover_circulo("izquierda")
            elif command == "derecha":
                mover_circulo("derecha")
    except Exception as e:
        print(f"Error: {str(e)}")

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

    # Esperar 0.1 segundos
    pg.time.delay(100)
