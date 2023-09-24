import cv2
import mediapipe as mp
import numpy as np
import pygame as pg

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Inicializa la cámara
cap = cv2.VideoCapture(0)

# Inicializa el modelo de detección de manos
hands = mp_hands.Hands()

# Configura el tamaño del cuadro para el mousepad
width, height = 640, 480
frame = np.zeros((height, width, 3), dtype=np.uint8)

# Definir las coordenadas del rectángulo (mousepad)
mousepad_x, mousepad_y, mousepad_width, mousepad_height = 100, 100, 440, 280

# Definir el tamaño de la cuadrícula del juego
grid_size = 3
cell_size = mousepad_width // grid_size

# Inicializar la posición del avatar en el centro de la cuadrícula
avatar_x, avatar_y = grid_size // 2, grid_size // 2

# Configuración de Pygame
pg.init()
pg_width, pg_height = 640, 480
pg_screen = pg.display.set_mode((pg_width, pg_height))
pg.display.set_caption("Control de Avatar con Mano")
pg_clock = pg.time.Clock()

while True:
    ret, image = cap.read()
    if not ret:
        continue

    # Voltea la imagen horizontalmente para que sea como un espejo
    image = cv2.flip(image, 1)

    # Procesa la imagen para detectar las manos
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Dibuja el rectángulo (mousepad)
    cv2.rectangle(image, (mousepad_x, mousepad_y), (mousepad_x + mousepad_width, mousepad_y + mousepad_height), (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtiene la posición del dedo índice
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Mapea la posición del dedo índice en el "mousepad" a la cuadrícula del juego
            avatar_x = int((index_finger.x * mousepad_width) / width)
            avatar_y = int((index_finger.y * mousepad_height) / height)

    # Dibuja el avatar en la cuadrícula
    avatar_x = min(max(0, avatar_x), grid_size - 1)
    avatar_y = min(max(0, avatar_y), grid_size - 1)

    # Limpiar la pantalla de Pygame
    pg_screen.fill((255, 255, 255))

    # Dibuja la cuadrícula del juego
    for x in range(grid_size):
        for y in range(grid_size):
            cell_x = mousepad_x + x * cell_size
            cell_y = mousepad_y + y * cell_size
            pg.draw.rect(pg_screen, (0, 0, 0), (cell_x, cell_y, cell_size, cell_size), 1)

    # Dibuja el avatar en la cuadrícula
    cell_x = mousepad_x + avatar_x * cell_size
    cell_y = mousepad_y + avatar_y * cell_size
    avatar_color = (255, 0, 0)
    pg.draw.circle(pg_screen, avatar_color, (cell_x + cell_size // 2, cell_y + cell_size // 2), cell_size // 2)

    # Muestra la imagen de la cámara
    cv2.imshow('Hand Tracking', image)

    # Actualiza la pantalla de Pygame
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pg.quit()
            exit(0)

    pg_clock.tick(60)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pg.quit()
