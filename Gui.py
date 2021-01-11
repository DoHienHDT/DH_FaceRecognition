from tkinter import *
import cv2
import numpy as np
import random
from PIL import Image, ImageTk

import face_recognition
import os
from datetime import datetime

root = Tk()
sizex = 450
sizey = 300
posx = 100
posy = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

f1 = LabelFrame(root, bg="red")
f1.pack(side=RIGHT)

f1 = LabelFrame(root, bg="red")
f1.pack(side=RIGHT)

L1 = Label(f1, bg="red")
L1.pack()

path = 'ImagesCompany'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
width = 1500
height = 1080
count = 0
button_label_list = []
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


while True:
    imgCap = cap.read()[1]
    imgCap = cv2.cvtColor(imgCap, cv2.COLOR_BGR2RGB)
    imgCap = ImageTk.PhotoImage(Image.fromarray(imgCap))
    L1['image'] = imgCap
    # root.add_widget(layout)
    root.update()
