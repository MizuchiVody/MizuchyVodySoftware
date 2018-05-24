import ImageRecognitionSystem as IRS
from tkinter import *
import datetime
from cv2 import *
from sys import *
from time import *
from numpy import *
from imutils import *
from serial import *
from collections import *
import pytesseract
import sympy as sp
import numpy as np
import math

def DetectText(img):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract"
    text1 = pytesseract.image_to_string(img, lang='eng')
    if(text1 != ''):
        text2 = "the extraxted text from the image is:\n" + text1
        print(text2)

def Missions():
    fields_1 = ('heading', 'ascent airspeed', 'ascent rate', 'engine failure time', 'decsent airspeed', 'decsent rate', 'wind heading', 'W(x)')
    fields_3 = ('number of turbines', 'water density', 'turbine radius', 'velocity in water', 'turbine efficiency')

    # functions for mission 1
    def ascentmovement(entries):
        h = float(entries['heading'].get())
        aas = float(entries['ascent airspeed'].get())
        t = float(entries['engine failure time'].get())
        global ycomp
        ycomp = aas * t * cos(deg2rad(h))
        global xcomp
        xcomp = aas * t * sin(deg2rad(h))
        print("ascent movement: ")
        print(xcomp)
        print(ycomp)

    def descentmovement(entries):
        aar = float(entries['ascent rate'].get())
        h = float(entries['heading'].get())
        das = float(entries['decsent airspeed'].get())
        t = float(entries['engine failure time'].get())
        t2 = (t * aar) / 6
        adr = float(entries['decsent rate'].get())
        global Ycomp
        Ycomp = das * t2 * cos(deg2rad(h))
        global Xcomp
        Xcomp = das * t2 * sin(deg2rad(h))
        print("descent movement: ")
        print(Xcomp)
        print(Ycomp)

    def windmovement(entries):
        aar = float(entries['ascent rate'].get())
        global h
        h = float(entries['heading'].get())
        das = float(entries['decsent airspeed'].get())
        t = float(entries['engine failure time'].get())
        t2 = (t * aar) / 6
        adr = float(entries['decsent rate'].get())
        Wt = str(entries['W(x)'].get())
        w = float(entries['wind heading'].get())
        x = sp.symbols('x')
        global ypos
        ypos = sp.integrate(Wt, (x, 0, t2)) * (cos(deg2rad(w - 180)))
        global xpos
        xpos = sp.integrate(Wt, (x, 0, t2)) * sin(deg2rad(w - 180))
        print("wind movement: ")
        print(xpos)
        print(ypos)

    def totmovement(entries):

        global xtot
        xtot = xcomp + Xcomp + xpos
        global ytot
        ytot = ycomp + Ycomp + ypos
        print("total movement:")
        print(xtot)
        print(ytot)

    # def degree (entries):							arctan (sum (sines) / sum (cosines))
    def result(entries):
        dist = math.sqrt(xtot ** 2 + ytot ** 2)
        k = xtot / ytot
        direction = rad2deg(math.atan(abs(k)))
        print('reported search zone :')
        print(dist)
        # print (direction)
        if (xtot > 0 and ytot < 0):
            # direction+=180
            direction = 180 - direction

        elif (xtot > 0 and ytot > 0):
            # direction+=90
            direction = 90 - direction

        elif (xtot < 0 and ytot > 0):
            # direction-=360
            direction = 360 - direction

        elif (xtot < 0 and ytot < 0):
            direction = 270 - direction

        print(direction)

    # functions for mission 3

    def doval(entries):
        N = float(entries['number of turbines'].get())
        d = float(entries['water density'].get())
        r = float(entries['turbine radius'].get())
        v = float(entries['velocity in water'].get())
        e = float(entries['turbine efficiency'].get())
        global P
        P = 0.5 * (N * d * pi * (r ** 2) * (v ** 3))
        rt1 = Tk()
        Label(rt1, text='Maximum power that could be generated is:')
        rt1.mainloop()
        # print("Maximum Power: %f" % float(P))

    def makeform_for_1(root, fields):
        entries = {}
        for field in fields_1:
            row = Frame(root)
            lab = Label(row, width=22, text=field + ": ", anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries

    def makeform_for_3(root, fields):
        entries = {}
        for field in fields_3:
            row = Frame(root)
            lab = Label(row, width=22, text=field + ": ", anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries

    def prompt1():
        global ents
        ents = makeform_for_1(root, fields_1)
        b1 = Button(root, text='validate',
                    command=lambda: [ascentmovement(ents), descentmovement(ents), windmovement(ents),
                                     totmovement(ents), result(ents)]).pack(side=LEFT, padx=5, pady=5)
        b3 = Button(root, text='Quit', command=root.quit).pack(side=LEFT, padx=5, pady=5)
        root.mainloop()

    def prompt3():
        global ents
        ents = makeform_for_3(root, fields_3)
        b1 = Button(root, text='validate', command=lambda: [doval(ents)]).pack(side=LEFT, padx=3, pady=3)
        b3 = Button(root, text='Quit', command=root.quit).pack(side=LEFT, padx=3, pady=3)
        root.mainloop()

    z = Label(root, text="which mission do you wish to complete?", padx=2, pady=2, anchor='n', height=3, width=70)
    z.pack()
    btn1 = Button(root, text="Mission 1", command=prompt1)
    btn1.config(height=3, width=20)
    btn1.pack()
    btn3 = Button(root, text="Mission 3", command=prompt3)
    btn3.config(height=3, width=20)
    btn3.pack()
    b1 = Button(root, text='validate', command=lambda: [ascentmovement(ents), descentmovement(ents), windmovement(ents), totmovement(ents),result(ents)])
    root.mainloop()

root = Tk()
label = Label(root)

cam1 = VideoCapture(0)
cam2 = VideoCapture(1)

width, height = maxsize, maxsize

cam1.set(CAP_PROP_FRAME_WIDTH, width)
cam1.set(CAP_PROP_FRAME_HEIGHT, height)

cam2.set(CAP_PROP_FRAME_WIDTH, 100)
cam2.set(CAP_PROP_FRAME_HEIGHT, 300)

cams = [cam1, cam2]

startTime = datetime.datetime.now()

index = 0
secCount = 0
min = 0
cnt = 0
show = 0

while(True):
    var, frame = cams[index].read()
    var, frame2 = cams[1 - index].read()

    frame[10:10 + frame2.shape[0], 10:10 + frame2.shape[1]] = frame2

    currSec = '0' + str(secCount) if secCount < 10 else str(secCount)

    currTime = '0' + str(min) + ':' + str(secCount) if min < 10 else str(min) + ':' + currSec

    putText(img=frame, text=currTime, org=(1000, 90), fontFace=FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=4,
            color=(210, 255, 215), thickness=4, lineType=CV_8S)

    timeElapsed = (datetime.datetime.now() - startTime).total_seconds()
    if (timeElapsed >= 1):
        secCount += 1
        timeElapsed = 0
        startTime = datetime.datetime.now()
    if (secCount == 60):
        secCount = 1
        min += 1

    k = waitKey(1) & 0xFF

    if(k == ord('m')):
        Missions()
    if (k == ord('t')):
        DetectText(frame)

    IRS.ProcessImage(frame)
    imshow('Frame', frame)

    if (k == 13 or k == ord('s')):
        index = 1 - index

        cams[index].set(CAP_PROP_FRAME_WIDTH, width)
        cams[index].set(CAP_PROP_FRAME_HEIGHT, height)

        cams[1 - index].set(CAP_PROP_FRAME_WIDTH, 100)
        cams[1 - index].set(CAP_PROP_FRAME_HEIGHT, 100)

    if (k == 27 or k == ord('Q') or k == ord('q')):  # Press ESC or Q to quit
        break


cam1.release()
cam2.release()
destroyAllWindows()