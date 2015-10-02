#!/usr/bin/python	
import numpy as np
# import pprint
# from graphics import *
from numpy.random import randint
import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from time import sleep
from time import time
# my files
import classdefs
import displayFunctions

winX = 400
winY = 400

## some API in the chain is translating the keystrokes to this octal string
# so instead of saying ESCAPE=27, we use the following
#   -from the pyopengl demo files
ESCAPE = '\033'


#  
# class Walker:
# 	#walkers exist on sidewalks. have a speed, a distination. 
# 	#and a wait tolerance aka how long they will wait to stay on the correct path
# 	def __init(self,curX=50, 
# 		self.curX = curX
# 		self.curY = curY
# 		self.nextDestX = curX
# 		self.nextDesty = curY
# 		self.finalDestX = finalDestX
# 		self.finalDestY = finalDestY
# 		self.speed = speed
# 		#wait tolerance is a formula for how long a walker will wait in order
# 		#to stay on the route with more theoretical remaining routes
# 		#wt = inf and the walker will always choose the corner 
# 		#wt = 0 and the walker will always cross at a stop light as long as
# 		#	it is no adding distance	

class Vehicle:
    def __init__(self, curX=50, curY=50, finalDestX=350, finalDestY=350, speed=1):
        self.curX = curX
        self.curY = curY
        self.nextDestX = curX
        self.nextDesty = curY
        self.finalDestX = finalDestX
        self.finalDestY = finalDestY
        self.speed = speed

    # wait tolerance = randint(15) once I figure out how to calculate
    # expected path time
    # right now they will just take the open light


class Intersection:
    def __init__(self, x, y, tm_x=30, tm_y=30, wd=40, ht=40, ):
        # important to use integers here and not a list of length two because of the immutable object problem that i dont fully understand
        self.tm_x = tm_x
        self.tm_y = tm_y
        if randint(2):
            self.dir = -1
            self.tmrm = randint(tm_x)
        else:
            self.dir = 1
            self.tmrm = randint(tm_y)
        self.x = float(x)
        self.y = float(y)
        self.wd = float(wd)
        self.ht = float(ht)
        self.init_tm = self.tmrm


def displayIntersection(i):
    # define the corners of the intersection using the xy coordinates and
    # the height and width of the intersction
    # x,y are the coordinates of the center of the intersection
    # l,r,t,b are the corners of the intersection
    x = i.x / (winX / 2) - 1
    y = i.y / (winY / 2) - 1
    r = i.wd / 2 / winX
    l = -r
    t = i.ht / 2 / winY
    b = -t

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(r + x, t + y, 0)
    glVertex3f(r + x, b + y, 0)
    glVertex3f(l + x, b + y, 0)
    glVertex3f(l + x, t + y, 0)
    glEnd()

    # draw lines indicating intesection direction
    glColor3f(1, 0, 0)
    # red line1 (flips when intersection flips)
    # based in upper left
    glBegin(GL_LINES)
    glVertex3f(l + x, t + y, 0)
    # this point moves to opposite corner when the light switches
    # at lower left when dir=0, upper right while dir=1
    glVertex3f(i.dir * l + x, i.dir * b + y, 0)
    glEnd()

    # redline2
    # based in lower right
    glBegin(GL_LINES)
    glVertex3f(r + x, b + y, 0)
    # this point moves to opposite corner when the light switches
    glVertex3f(i.dir * r + x, i.dir * t + y, 0)
    glEnd()

    # green line 1
    # based in upper right
    glColor3f(0, 1, 0)
    glBegin(GL_LINES)
    glVertex3f(r + x, t + y, 0)
    # left top when dir=1, righ bottom when dir = =-1
    glVertex(i.dir * l + x, i.dir * t + y, 0)
    glEnd()

    # green line 2
    # based in bottom left
    glBegin(GL_LINES)
    glVertex3f(l + x, b + y, 0)
    glVertex3f(i.dir * r + x, i.dir * b + y, 0)
    glEnd()

    glColor3f(0, 0, 0)
    glWindowPos3f(i.x - 7, i.y - 5, 0)
    for c in str(i.tmrm):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))


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

    sleep(1 / float(frameRate))
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # draw intersection rectangles
    for street in Intersections:
        for i in street:
            displayIntersection(i)

    glutSwapBuffers()


frameRate = 20
init_time = int(time())
dur = 0

# initialize set of intersections
Intersections = [[Intersection(x, y) for x in range(50, 400, 100)] for y in range(50, 400, 100)]

print Intersections[2][3].x
print Intersections[2][3].y


# for x in range(50,400,100):
#	for y in range(50,400,100):
#		Intersections.append(Intersection(x,y))




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
