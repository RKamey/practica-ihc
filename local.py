# intento por hacer reconocimiento con librerias locales

#https://alphacephei.com/vosk/models
from vosk import Model, KaldiRecognizer
# pyaudio
import pyaudio

# usamos el modelo de la libreria vosk que es el archivo que descargamos
# r se usa porque es una ruta de la carpeta que estamos usando
model = Model(r"C:\Users\JorgeCR\Documents\vosk-model-small-es-0.42\vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text)
        print(text[14:-3])

