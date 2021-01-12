from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import face_recognition
import os
import PIL
from datetime import datetime
from autocrop import Cropper

def addBox():
    # I use len(all_entries) to get nuber of next free column

    ent = Button(window, image=imgShowDemo)
    arrayButton.insert(0, ent)

    i = 0
    for item in arrayButton:
        i += 1
        button = item
        box_row = i * 2 + 1
        button.grid(row=box_row, column=1)

    # next_column = len(all_entries)
    #
    # # add label in first row
    # lab = Label(window, text=str(next_column + 1))
    # text_row = next_column * 2 + 2
    # lab.grid(row=text_row, column=1)
    #
    #
    #
    # # add entry in second row
    # ent = Button(window, image=imgShowDemo)
    # box_row = next_column * 2 + 1
    # ent.grid(row=index-1, column=1)
    #
    # all_entries.append(ent)


root = Tk()
lmain = Label(root)
lmain.pack(side="right")
timeSleep = 0
path = 'ImagesCompany'
images = []
imagesDetect = []
arrayButton = []
classNames = []
all_entries = []
myList = os.listdir(path)
print(myList)

frameAddBox = Frame(root, relief=GROOVE, width=550, height=50, bd=1, bg="white")
frameAddBox.place(x=10, y=30)

canvas = Canvas(frameAddBox, bg="white")

File = "cropped.png"
imgShowDemo = ImageTk.PhotoImage(Image.open(File))

addboxButton = Button(root, text='<Add Time Input>', fg="Red", command=addBox, highlightbackground='#3E4149')
addboxButton.pack()


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=1150)


window = Frame(canvas, bg="white")
scrollbarBox = Scrollbar(frameAddBox, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbarBox.set)
scrollbarBox.pack(side="right", fill="y")
canvas.pack(side="left")
canvas.create_window((0, 0), window=window, anchor='nw')
window.bind("<Configure>", myfunction)



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

width, height = 1700, 1280
cropper = Cropper()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    success, frame = cap.read()
    imgS = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            sortName = np.sort(faceDis)
            medium = sortName[int(sortName.size / 2)]

            # print(faceDis[matchIndex], medium, medium - faceDis[matchIndex])

            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)

            if medium - faceDis[matchIndex] > 0.2:
                cv2.putText(frame, name[:-2], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, str(datetime.now()), (x1 + 6, y2 + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                            2)

                timeSleep += 1

                if timeSleep % 10 == 0:
                    cv2.imwrite('HistoryFaceDetect/' + name[:-2] + '.jpg', frame)
                #     ent = Button(window, image=imgShowDemo)
                #     arrayButton.insert(0, ent)
                #
                #     indexImage = 0
                #     for item in arrayButton:
                #         indexImage += 1
                #         button = item
                #         box_row = indexImage * 2 + 1
                #         button.grid(row=box_row, column=1)

                # cv2.imwrite('HistoryFaceDetect/' + name[:-2] + '.jpg', img)
            else:
                cv2.putText(frame, str(datetime.now()), (x1 + 6, y2 + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                            2)
                cv2.putText(frame, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # cv2.imwrite('HistoryFaceDetect/' + name[:-2] + '.jpg', img)
            cv2.putText(frame, f'{round(faceDis[matchIndex], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 255), 2)

    # frameFlip = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.update()