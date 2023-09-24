import pygame as pg # Importamos pygame y lo llamamos pg
import pyaudio
from random import randrange # Importamos la función randrange del módulo random
from vosk import Model, KaldiRecognizer

WINDOW = 800 # Definimos la ventana
TILE_SIZE = 50 # Definimos el tamaño de la celda
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE) # Definimos el rango de la celda
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)] # Definimos una función lambda para obtener una posición aleatoria
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE -2]) # Definimos la serpiente
snake.center = get_random_position() # Centramos la serpiente
length = 1 # Definimos la longitud de la serpiente
segments = [snake.copy()] # Definimos los segmentos de la serpiente
snake_dir = (0, 0) # Definimos la dirección de la serpiente
time, time_step = 0, 110 # Definimos el tiempo y el paso de tiempo
food = snake.copy() # Definimos la comida
food.center = get_random_position() # Centramos la comida
icon = pg.image.load('./images/snake.png') # Cargamos el icono
pg.display.set_icon(icon) # Definimos el icono
screen = pg.display.set_caption('Practica 1: Snake con Reconocimiento de Voz') # Definimos el título de la pantalla
screen = pg.display.set_mode([WINDOW] * 2) # Definimos la pantalla
clock = pg.time.Clock() # Definimos el reloj

# Definimos el modelo para el reconocimiento de voz en español
model = Model(r"C:\Users\alons\Downloads\vosk-model-small-es-0.42\vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

# Configuramos el audio del micrófono
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

def move_snake(direction):
    global snake_dir

    if direction == "arriba":
        snake_dir = (0, -TILE_SIZE)
    elif direction == "abajo":
        snake_dir = (0, TILE_SIZE)
    elif direction == "izquierda":
        snake_dir = (-TILE_SIZE, 0)
    elif direction == "derecha":
        snake_dir = (TILE_SIZE, 0)

while True: # Bucle principal
    for event in pg.event.get(): # Bucle de eventos
        if event.type == pg.QUIT: # Si el evento es cerrar la ventana
            exit() # Salimos del programa
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                command = recognizer.Result().lower().strip()

                if "arriba" in command:
                    print("Comando: ", command)
                    move_snake("arriba")
                elif "abajo" in command:
                    print("Comando: ", command)
                    move_snake("abajo")
                elif "izquierda" in command:
                    print("Comando: ", command)
                    move_snake("izquierda")
                elif "derecha" in command:
                    print("Comando: ", command)
                    move_snake("derecha")

        except Exception as e:
            print(f"Error: {str(e)}")

    
    screen.fill('black') # El fondo es negro

    # check borders and selfeating
    self_eating = any(snake.colliderect(segment) for segment in segments[:-1]) 
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
    # check food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
    # draw food
    pg.draw.rect(screen, 'red', food)
    # draw snake
    [pg.draw.rect(screen, 'green', segment) for segment in segments]
    # move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    
    pg.display.flip()
    clock.tick(60)