# Menú para el juego
import pygame as pg

# Inicializamos pygame
pg.init()

# Tamaño de la ventana
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Menú principal")

# Colores
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
hover_red = (255, 100, 100)  # Color cuando el cursor está sobre el botón

# Fuente para el texto
font = pg.font.Font(None, 36)

# Texto del menú
title_text = font.render("Menú principal", True, white)
start_text = font.render("Iniciar juego", True, white)
exit_text = font.render("Salir", True, white)

# Rectángulos para los botones
title_rect = title_text.get_rect(center=(width // 2, 100))
start_rect = start_text.get_rect(center=(width // 2, 300))
exit_rect = exit_text.get_rect(center=(width // 2, 400))

# Bucle principal
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    # Obtiene la posición del mouse
    mouse_pos = pg.mouse.get_pos()

    # Verifica si el mouse está sobre el botón de iniciar
    if start_rect.collidepoint(mouse_pos):
        start_text = font.render("Iniciar juego", True, hover_red)
        if pg.mouse.get_pressed()[0]:  # Detecta si se hizo clic
            print("Iniciar juego")
    else:
        start_text = font.render("Iniciar juego", True, white)

    # Verifica si el mouse está sobre el botón de salir
    if exit_rect.collidepoint(mouse_pos):
        exit_text = font.render("Salir", True, hover_red)
        if pg.mouse.get_pressed()[0]:  # Detecta si se hizo clic
            running = False
    else:
        exit_text = font.render("Salir", True, white)

    # Limpiar la pantalla
    screen.fill(black)

    # Dibujar los textos
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)

    # Actualizar la pantalla
    pg.display.flip()

# Salir del juego
pg.quit()