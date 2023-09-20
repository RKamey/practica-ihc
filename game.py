import pygame as pg # Importamos pygame y lo llamamos pg
import speech_recognition as sr # Importamos speech_recognition y lo llamamos sr
from random import randrange # Importamos la función randrange del módulo random

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

# Definimos un diccionario para mapear las teclas con las direcciones
key_map = { 
    pg.K_w: (0, -TILE_SIZE), 
    pg.K_s: (0, TILE_SIZE), 
    pg.K_a: (-TILE_SIZE, 0), 
    pg.K_d: (TILE_SIZE, 0) 
} 

recognizer = sr.Recognizer() # Definimos el reconocedor

while True: # Bucle principal
    for event in pg.event.get(): # Bucle de eventos
        if event.type == pg.QUIT: # Si el evento es cerrar la ventana
            exit() # Salimos del programa
        if event.type == pg.KEYDOWN and event.key in key_map:
            new_direction = key_map[event.key]
            if (new_direction != (-snake_dir[0], -snake_dir[1])):
                snake_dir = new_direction
    
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