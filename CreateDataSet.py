import cv2
import os
from tkinter import *
import PIL
from PIL import Image, ImageTk

root = Tk()
root.geometry("1920x1080")
lmain = Label(root)
lmain.pack(side="right", anchor=NW)

cam = cv2.VideoCapture(0)
cam.set(3, 1920)  # set video width
cam.set(4, 1080)  # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')

count = 0
delay = 0

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        delay += 1

        if delay % 4 == 0:
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

    if count >= 100:  # Take 30 face sample and stop video
        break

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.update()