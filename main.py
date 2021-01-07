# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw
import os

from datetime import datetime

# from PIL import ImageGrab

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

# logging.basicConfig(filename='logs.log',
#             filemode='w',
#             level=logging.INFO)

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    # img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            sortName = np.sort(faceDis)
            medium = sortName[int(sortName.size / 2)]

            print(faceDis[matchIndex], medium, medium - faceDis[matchIndex])

            name = classNames[matchIndex].upper()
            # print(faceDis)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)

            if medium - faceDis[matchIndex] > 0.2:
                # logging.info(name[:-2])
                cv2.putText(img, name[:-2], (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.imwrite('SaveImage/'+name[:-2]+'.jpg', img)
            else:
                cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(img, f'{round(faceDis[matchIndex], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 255), 2)

    imgl = Image.new('RGB', (100, 30), color=(73, 109, 137))

    d = ImageDraw.Draw(imgl)
    d.text((10, 10), "Hello World", fill=(255, 255, 0))

    imgl.save('pil_text.png')

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
