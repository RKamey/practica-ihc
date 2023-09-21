import speech_recognition

recognizer = speech_recognition.Recognizer()
# esto crea un ciclo que accedde al audio del microfrono en tiempo real para 
# escribir por consola lo que estoy hablando
while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            
            text = recognizer.recognize_google(audio)
            text = text.lower()

            print(f"Recognized {text}")
    except speech_recognition.UnknownValueError():
        recognizer = speech_recognition.Recognizer()
        continue