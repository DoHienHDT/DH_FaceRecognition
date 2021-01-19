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
        Button(window, image=imageArray).grid(row=box_row, column=1, ipadx=50)

    j = 0
    for timeCheck in dateCHeck:
        j += 1
        text_row = j * 2 + 2
        Label(window, text=timeCheck).grid(row=text_row, column=1, pady=20)


root = Tk()
root.geometry("1400x850")
lmain = Label(root)
lmain.pack(side="right", anchor=NW)
timeSleep = 0
timeUnknow = 0
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
    canvas.configure(scrollregion=canvas.bbox("all"), width=450, height=1150)


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
        imageOpen = imageOpen.resize((300, 300), Image.ANTIALIAS)
        addImageArray = ImageTk.PhotoImage(imageOpen)
        imagesHistory.insert(0, addImageArray)

    if len(imagesHistory) != 0:
        addBox(imagesHistory, dateCHeck)


with open('dataset_faces.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)

# Create arrays of known face encodings and their names
encodeListKnown = all_face_encodings
encodeListKnown = np.array(list(all_face_encodings.values()))

# Get a reference to webcam #0 (the default one)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)

while True:
    # Grab a single frame of video
    success, frame = cap.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    imgS = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = imgS[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        encodesCurFrame = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for encodeFace, faceLoc in zip(encodesCurFrame, face_locations):

            # See if the face is a match for the known face(s)
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
                        # Name and Datetime
                        dateDetect = f'{name[:-2]}_{str(datetime.now())}'

                        # Appends to the first position of the array
                        dateArrayHistory.insert(0, dateDetect)

                        # clear image in fouder
                        clearFounder()

                        # clear ui history capture image
                        clearFrame()

                        # save image to file
                        cv2.imwrite('HistoryFaceDetect/' + name[:-2] + '.jpg', frame)

                        # read file after save image load ui
                        readFileImage(dateArrayHistory)
                        timeSleep = 0
                    else:
                        # save name show realtime with camera
                        face_names.append(name)
                else:
                    timeUnknow += 1
                    if timeUnknow % 10 == 0:

                        dateDetect = f'Hello_Person_{str(datetime.now())}'

                        dateArrayHistory.insert(0, dateDetect)

                        clearFounder()
                        clearFrame()

                        cv2.imwrite('HistoryFaceDetect/' + name[:-2] + '.jpg', frame)

                        readFileImage(dateArrayHistory)
                        timeUnknow = 0
                    else:
                        name = "Unknown"
                        face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), nameBox in zip(face_locations, face_names):

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if nameBox == "Unknown":
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, nameBox, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            # cv2.putText(frame, name1[:-2], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, nameBox[:-2], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    root.update()
