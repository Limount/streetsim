#!/usr/bin/python

import numpy as np

from numpy.random import randint
import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from time import sleep
from time import time
# my files\
from classdefs import *
from displayFunctions import *
from globalvars import winX,winY,frameRate

## some API in the chain is translating the keystrokes to this octal string
# so instead of saying ESCAPE=27, we use the following
#   -from the pyopengl demo files
ESCAPE = '\033'


def doAnimationStep():
    global Intersections
    global dur
    current_time = int(time())
    if dur != (current_time - init_time):
        dur = current_time - init_time
        for street in Intersections:
            for i in street:
                i.tmrm -= 1
                if i.tmrm == -1:
                    if i.dir > 0:
                        i.tmrm = i.tm_x
                    else:
                        i.tmrm = i.tm_y
                    i.dir = -i.dir
        for v in Vehicles:
            v.y+=v.speed
    sleep(1 / float(frameRate))
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    global winX, winY
    displayRoads(Intersections)
    # draw intersection rectangles
    for street in Intersections:
        for i in street:
            displayIntersection(i, winX, winY)

    displayVehicles(Vehicles)

    glutSwapBuffers()



init_time = int(time())
dur = 0

# initialize set of intersections


Intersections = [[Intersection(x, y) for x in range(50, winX, 100)] for y in range(50, winY, 100)]
Vehicles = [Vehicle(),Vehicle(120,100)]
#Intersections[2][3] = Intersection(350,250,20,20,100,00)

# initialize the window
def init():
    glClearColor(0.5, 0.5, 0.5, 1)
    glShadeModel(GL_SMOOTH)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(winX, winY)

glutCreateWindow(sys.argv[0])
init()
glutDisplayFunc(display)
glutIdleFunc(doAnimationStep)
glutMainLoop()
