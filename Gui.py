from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import time
from scrollimage import ScrollableImage

root = Tk()
root.geometry("600x540")
root.configure(bg="white")
# Button(root, text="Take Snapshot", font=("times new roman", 20, 'bold'), bg="black",fg="red").pack()
f1 = LabelFrame(root, bg="red")
f1.pack(side=RIGHT)

text = Text(root, wrap="none")
vsb = Scrollbar(orient="vertical", command=text.yview)
text.configure(yscrollcommand=vsb.set)
vsb.pack(side=LEFT, fill="y")
text.pack(side=LEFT, expand=True)

for i in range(20):
    b =  Button(root, text="Button #%s" % i, highlightbackground='#3E4149')
    text.window_create("end", window=b, pady=10)
    text.insert("end", "\n")

text.configure(state="disabled")

def add_timestamp(self):
    fully_scrolled_down = self.text.yview()[1] == 1.0
    self.text.insert("end", time.ctime() + "\n")
    if fully_scrolled_down:
        self.text.see("end")
    self.after(1000, self.add_timestamp)


L1 = Label(f1, bg="red")
L1.pack()
cap = cv2.VideoCapture(0)
width = 1500
height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    img = cap.read()[1]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img))
    L1['image'] = img
    # root.add_widget(layout)
    root.update()
