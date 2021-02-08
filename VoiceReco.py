import speech_recognition as sr

def Destination():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now:")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return "Sorry, can't locate it."
