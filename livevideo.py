import face_recognition
import cv2
import os
import pickle
import time
import pyttsx3
from adafruit_servokit import ServoKit

kit = ServoKit(channels = 16)

Encodings = []
Names = []

with open('train.pkl','rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)
font = cv2.FONT_HERSHEY_COMPLEX

j = 1


cam = cv2.VideoCapture(0)
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
pan = 90
tilt = 90


kit.servo[0].angle = pan
kit.servo[1].angle = tilt



while True:
    _, frame = cam.read()
    frameSmall = cv2.resize(frame,(0,0),fx=.33,fy=.33)
    frameRGB = cv2.cvtColor(frameSmall, cv2.COLOR_BGR2RGB)

    facePositions = face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
        name = 'Unknown Person'

        matches = face_recognition.compare_faces(Encodings, face_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = Names[first_match_index]
            if name and j == 1:
                text = f'Well hello {name}, My name is Mr. Roboto'
                speak(text)
                j -= 1
        top = top*3
        right = right * 3
        bottom = bottom * 3
        left = left * 3
        
        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
        objX = (right + left) /2 #center x object
        objY = (bottom + top) /2 # center y object
        errorX = objX - (width /2)
        errorY = objY - (height / 2)

        if abs(errorX)>15:
            pan = pan-errorX/40

        if abs(errorY)>15:
             tilt = tilt + errorY/40

        if pan >180:
            pan = 180
        if pan < 0:
            pan = 0

        if tilt > 180:
            tilt = 180
        if tilt < 0:
            tilt = 0    


        kit.servo[0].angle = pan
        kit.servo[1].angle =tilt
            

        
            
        cv2.putText(frame,name,(left,top-6),font,.75,(255,0,0),2)
        
    cv2.imshow('Window',frame)
    cv2.moveWindow('Window',0,0)

 
 
    if cv2.waitKey(0) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()


