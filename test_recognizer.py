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
width, height = 600, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Juego con reconocimiento de voz")
pg.display.set_icon(pg.image.load("./images/voice.png"))

# Colores
white = (255, 255, 255)
red = (255, 0, 0)

# Tamaño de la cuadrícula
grid_size = 3
cell_size = width // grid_size

# Calcula la posición inicial del avatar en el centro
avatar_x = grid_size // 2
avatar_y = grid_size // 2

# Personaliza el avatar
avatar_image = pg.image.load("./images/snake.png")

# Define el nuevo tamaño del avatar
avatar_width = 200  # Ancho deseado
avatar_height = 200  # Alto deseado

# Función para mover el avatar
def move_avatar(direction):
    global avatar_x, avatar_y

    if direction == "derecha" and avatar_x < grid_size - 1:
        avatar_x += 1
    elif direction == "izquierda" and avatar_x > 0:
        avatar_x -= 1
    elif direction == "abajo" and avatar_y < grid_size - 1:
        avatar_y += 1
    elif direction == "arriba" and avatar_y > 0:
        avatar_y -= 1

# Bucle principal del juego
while True:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            pg.quit()
            quit()
    
    try:
        # Leer el audio del micrófono
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            command = (recognizer.Result()[14:-3]).lower()

            # Mover el avatar según el comando que escuchó el modelo
            if command == "arriba":
                move_avatar("arriba")
            elif command == "abajo":
                move_avatar("abajo")
            elif command == "izquierda":
                move_avatar("izquierda")
            elif command == "derecha":
                move_avatar("derecha")
    
    # Manejar errores
    except Exception as e:
        print(f"Error: {str(e)}")

    # Limpiar la pantalla
    screen.fill((255, 255, 255))

  # Dibuja la cuadrícula
    screen.fill(white)
    for x in range(grid_size):
        for y in range(grid_size):
            pg.draw.rect(screen, red, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    # Redimensiona y dibuja el avatar en la posición actual
    avatar_resized = pg.transform.scale(avatar_image, (avatar_width, avatar_height))
    avatar_position = (avatar_x * cell_size, avatar_y * cell_size)
    screen.blit(avatar_resized, avatar_position)

    # Actualizar la pantalla
    pg.display.flip()

    # Esperar 0.1 segundos
    pg.time.delay(100)
