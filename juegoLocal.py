import pygame
from vosk import Model, KaldiRecognizer
import pyaudio
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

# Inicializa el modelo y el reconocedor Vosk
model = Model(r"C:\Users\JorgeCR\Documents\vosk-model-small-es-0.42\vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

# Función para mover el avatar
# Función para mover el avatar
def move_avatar(command):
    global avatar_x, avatar_y

    if "derecha" in command and avatar_x < grid_size - 1:
        avatar_x += 1
    elif "izquierda" in command and avatar_x > 0:
        avatar_x -= 1
    elif "abajo" in command and avatar_y < grid_size - 1:
        avatar_y += 1
    elif "arriba" in command and avatar_y > 0:
        avatar_y -= 1


# Configura PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

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

    # Reconocimiento de voz con Vosk
    audio_data = stream.read(8000)
    if len(audio_data) > 0:
        if recognizer.AcceptWaveform(audio_data):
            result = recognizer.Result()
            command = result.lower()
            print(f"Comando reconocido: {command}")
            move_avatar(command)

    pygame.display.flip()

# Cierra Pygame
pygame.quit()

# Cierra PyAudio
stream.stop_stream()
stream.close()
p.terminate()
