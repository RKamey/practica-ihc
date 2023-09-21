import pygame
import speech_recognition as sr
import time

# Inicializa pygame
pygame.init()

# Configuración de la pantalla
width, height = 300, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego de Comandos de Voz")

# Colores
white = (255, 255, 255)
red = (255, 0, 0)

# Tamaño de la cuadrícula
grid_size = 3
cell_size = width // grid_size

# Calcula la posición inicial del avatar en el centro
avatar_x = grid_size // 2
avatar_y = grid_size // 2

# Inicializa el reconocimiento de voz
recognizer = sr.Recognizer()

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

# Loop principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibuja la cuadrícula
    screen.fill(white)
    for x in range(grid_size):
        for y in range(grid_size):
            pygame.draw.rect(screen, red, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    # Dibuja el avatar en la posición actual
    avatar_rect = pygame.Rect(avatar_x * cell_size, avatar_y * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, red, avatar_rect)

    # Reconocimiento de voz
    with sr.Microphone() as source:
        print("Di un comando de voz:")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)  # Espera hasta 5 segundos
            command = recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"Comando reconocido: {command}")
            move_avatar(command)
        except sr.WaitTimeoutError:
            print("Tiempo de espera de entrada de voz agotado.")
        except sr.UnknownValueError:
            print("No se pudo entender el comando de voz.")
        except sr.RequestError as e:
            print(f"Error en la solicitud de reconocimiento de voz: {e}")

    pygame.display.flip()

# Cierra pygame
pygame.quit()
