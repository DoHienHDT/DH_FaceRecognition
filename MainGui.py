from tkinter import *
import cv2
import numpy as np
import random
from PIL import Image, ImageTk
import tkinter as tk
import random


def addBox():
    # I use len(all_entries) to get nuber of next free column
    next_column = len(all_entries)

    # add label in first row
    lab = Label(window, text=str(next_column + 1))
    text_row = next_column * 2 + 2
    lab.grid(row=text_row, column=1)

    # add entry in second row

    ent = Button(window, text="news", image=img)
    # ent = Entry(window)
    box_row = next_column * 2 + 1
    ent.grid(row=box_row, column=1)

    all_entries.append(ent)


all_entries = []

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

canvas = Canvas(myframe, bg="white")

File = "cropped.png"
img = ImageTk.PhotoImage(Image.open(File))

f1 = LabelFrame(root, bg="red")
f1.pack(side=RIGHT)

f1 = LabelFrame(root, bg="red")
f1.pack(side=RIGHT)

L1 = Label(f1, bg="red")
L1.pack()

# setup face detect


cap = cv2.VideoCapture(0)
width = 1500
height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=1150)


window = Frame(canvas, bg="white")
myscrollbar = Scrollbar(myframe, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar.pack(side="right", fill="y")
canvas.pack(side="left")
canvas.create_window((0, 0), window=window, anchor='nw')
window.bind("<Configure>", myfunction)

while True:
    imgCap = cap.read()[1]
    imgCap = cv2.cvtColor(imgCap, cv2.COLOR_BGR2RGB)
    imgCap = ImageTk.PhotoImage(Image.fromarray(imgCap))
    L1['image'] = imgCap
    root.update()
