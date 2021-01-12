from tkinter import *
import cv2
import numpy as np
import random
from PIL import Image, ImageTk
import tkinter as tk
import os
from autocrop import Cropper


def addBox():

    # I use len(all_entries) to get nuber of next free column
    # clearFrame()

    # ent = Button(window, text="news", image=img)
    # arrayButton.insert(0, ent)

    i = 0

    for imgDeno in images:
        i += 1
        box_row = i * 2 + 1
        Button(window, text="news", image=imgDeno).grid(row=box_row, column=1)

    # for item in arrayButton:
    #     i += 1
    #     button = item
    #     box_row = i * 2 + 1
    #     button.grid(row=box_row, column=1)


    # next_column = len(all_entries)
    #
    # # add label in first row
    # lab = Label(window, text=str(next_column + 1))
    # text_row = next_column * 2 + 2
    # lab.grid(row=text_row, column=1)
    #
    # # add entry in second row
    #
    # ent = Button(window, text="news", image=img)
    # arrayButton.append(ent)
    # # ent = Entry(window)
    # box_row = next_column * 2 + 1
    # ent.grid(row=box_row, column=1)
    #
    # all_entries.append(ent)


all_entries = []
arrayButton = []
root = Tk()
sizex = 450
sizey = 300
posx = 100
posy = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe = Frame(root, relief=GROOVE, width=550, height=50, bd=1, bg="white")
myframe.place(x=10, y=30)

addboxButton = Button(root, text='<Add Time Input>', fg="Red", command=addBox, highlightbackground='#3E4149')
addboxButton.pack()


def clearFrame():
    for widget in window.winfo_children():
        widget.destroy()


Button(myframe, text="clear frame", command=clearFrame).pack()

canvas = Canvas(myframe, bg="white")

images = []
path = 'HistoryFaceDetect'
myList = os.listdir(path)
for cl in myList:
    # curImg = cv2.imread(f'{path}/{cl}')
    nameFile = f'{path}/{cl}'
    imgAdd = ImageTk.PhotoImage(Image.open(nameFile))
    images.append(imgAdd)

File = "HistoryFaceDetect/croppedpng66.png"
img = ImageTk.PhotoImage(Image.open(File))

# cropper = Cropper()
#
# # Get a Numpy array of the cropped image
# cropped_array = cropper.crop('HistoryFaceDetect/DOHIEN.jpg')
#
# # Save the cropped image with PIL
# img = Image.fromarray(cropped_array)


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=1150)


myscrollbar = Scrollbar(myframe, orient="vertical", command=canvas.yview)
window = Frame(canvas, bg="white")
canvas.create_window((0, 0), window=window, anchor='nw')
window.bind("<Configure>", myfunction)

canvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar.pack(side="right", fill="y")
canvas.pack(side="left")

while True:
    root.update()
