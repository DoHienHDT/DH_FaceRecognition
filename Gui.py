from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import face_recognition
import os
import PIL
import asyncio
import shutil
from datetime import datetime
import pickle


def addBox(arrayImageHistory, dateCHeck):
    # I use len(all_entries) to get number of next free column
    i = 0
    for imageArray in arrayImageHistory:
        i += 1
        box_row = i * 2 + 1
        Button(window, image=imageArray).grid(row=box_row, column=1)

    j = 0
    for timeCheck in dateCHeck:
        j += 1
        text_row = j * 2 + 2
        Label(window, text=timeCheck).grid(row=text_row, column=1)


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

face_locations = []
face_names = []

myList = os.listdir(path)
print(myList)

frameAddBox = Frame(root, relief=GROOVE, width=550, height=50, bd=1, bg="white")
frameAddBox.place(x=10, y=30)

canvas = Canvas(frameAddBox, bg="white")


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=250, height=1150)


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


def findEncodings(imagesEndcoding):
    encodeList = []
    for imgArray in imagesEndcoding:
        imgCVT = cv2.cvtColor(imgArray, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(imgCVT)[0]
        encodeList.append(encode)
    return encodeList


def clearFrame():
    for widget in window.winfo_children():
        widget.destroy()


def clearFounder():
    for rootFile, dirs, files in os.walk('HistoryFaceDetect'):
        for f in files:
            os.unlink(os.path.join(rootFile, f))
        for d in dirs:
            shutil.rmtree(os.path.join(rootFile, d))


pathHisotry = 'HistoryFaceDetect'
imagesHistory = []
dateArrayHistory = []
process_this_frame = True


def readFileImage(dateCHeck):
    myList = os.listdir(pathHisotry)
    for clArray in myList:
        nameFile = f'{pathHisotry}/{clArray}'
        imageOpen = Image.open(nameFile)
        imageOpen = imageOpen.resize((200, 200), Image.ANTIALIAS)
        addImageArray = ImageTk.PhotoImage(imageOpen)
        imagesHistory.insert(0, addImageArray)

    if len(imagesHistory) != 0:
        addBox(imagesHistory, dateCHeck)


with open('dataset_faces.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)

encodeListKnown = all_face_encodings
encodeListKnown = np.array(list(all_face_encodings.values()))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    success, frame = cap.read()
    imgS = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    if process_this_frame:
        face_locations = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, face_locations)

        face_names = []
        for encodeFace, faceLoc in zip(encodesCurFrame, face_locations):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                sortName = np.sort(faceDis)
                medium = sortName[int(sortName.size / 2)]
                name = classNames[matchIndex].upper()

                if medium - faceDis[matchIndex] > 0.2:
                    timeSleep += 1
                    if timeSleep % 15 == 0:

                        dateDetect = f'{name[:-2]}_{str(datetime.now())}'

                        dateArrayHistory.insert(0, dateDetect)

                        clearFounder()
                        clearFrame()

                        cv2.imwrite('HistoryFaceDetect/' + name[:-2] + '.jpg', frame)

                        readFileImage(dateArrayHistory)
                    else:
                        face_names.append(name)
                else:
                    name = "Unknown"
                    face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for faceLoc1, name1 in zip(face_locations, face_names):
        y1, x2, y2, x1 = faceLoc1
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        if name1 == "Unknown":
            cv2.putText(frame, name1, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            cv2.putText(frame, name1[:-2], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.update()
