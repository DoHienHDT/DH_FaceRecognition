import os
import cv2
import pickle
import face_recognition
import numpy as np

all_face_encodings = {}
classNames = []
# images = []
path = 'ImagesCompany'
myList = os.listdir(path)
#
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    classNames.append(os.path.splitext(cl)[0])
    imgCVT = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
    all_face_encodings[os.path.splitext(cl)[0]] = face_recognition.face_encodings(imgCVT)[0]

with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)

# Load face encodings

# https://github.com/ageitgey/face_recognition/issues/243

# with open('dataset_faces.dat', 'rb') as f:
# 	all_face_encodings = pickle.load(f)
#
# # Grab the list of names and the list of encodings
# face_names = list(all_face_encodings.keys())
# face_encodings = np.array(list(all_face_encodings.values()))
#
# # Try comparing an unknown image
# unknown_image = face_recognition.load_image_file("ImagesCompany/Dung02.jpg")
# unknown_face = face_recognition.face_encodings(unknown_image)
# result = face_recognition.compare_faces(face_encodings, unknown_face)
#
# # Print the result as a list of names with True/False
# names_with_result = list(zip(face_names, result))
# print(names_with_result)