import os 
import pyttsx3

def speak(text):
     engine = pyttsx3.init()
     rate = engine.getProperty('rate')
     engine.setProperty('rate',rate - 50)

     volume = engine.getProperty('volume')
     engine.setProperty('volume',volume)

     voices = engine.getProperty('voices')
     engine.setProperty('voice',voices[2].id)
     
     engine.say(text)
     engine.runAndWait()


text = 'Sweet dreams little Leo!'
speak(text)

