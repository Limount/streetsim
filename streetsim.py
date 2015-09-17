#!/usr/bin/python	
import numpy as np
#import pprint
#from graphics import *
from numpy.random import randint
import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from time import sleep
from time import time

winX=400
winY=400

## some API in the chain is translating the keystrokes to this octal string
#so instead of saying ESCAPE=27, we use the following
#   -from the pyopengl demo files
ESCAPE = '\033'


class Intersection:
	def __init__(self,x,y,tm_x=5,tm_y=5,wd=40,ht=40,):
		#important to use integers here and not a list of length two because of the immutable object problem that i dont fully understand
		self.tm_x = tm_x
		self.tm_y = tm_y
		if randint(2):
			self.dir = -1
			self.tmrm = randint(tm_x)
		else:
			self.dir =1
			self.tmrm = randint(tm_y)
		self.x = float(x)
                self.y = float(y)
		self.wd = float(wd)
		self.ht = float(ht)
		self.init_tm = self.tmrm


#block size 500 ft base
#intersectiopn size 50ft
#speed 5 ft/s
# so i guess you can divide that all by 5 and it really prett and reasonable

def displayIntersection(i):
	r = i.wd/2/winX
	l = -r
	t = i.ht/2/winY
	b = -t



	glColor3f(1,1,1)
	glBegin(GL_QUADS)
	glVertex3f(r,t,0)
	glVertex3f(r,b,0)
	glVertex3f(l,b,0)
	glVertex3f(l,t,0)
	glEnd()

	#draw lines indicating intesection direction
	glColor3f(1,0,0)
	#red line1 (flips when intersection flips)
	#based in upper left
	glBegin(GL_LINES)
	glVertex3f(l,t,0)
	#this point moves to opposite corner when the light switches
	#at lower left when dir=0, upper right while dir=1
	glVertex3f(i.dir*l,i.dir*b,0)
   	glEnd()

	#redline2
	#based in lower right
	glBegin(GL_LINES)
	glVertex3f(r,b,0)
	#this point moves to opposite corner when the light switches
	glVertex3f(i.dir*r,i.dir*t,0)
	glEnd()
	
	#green line 1
	#based in upper right
	glColor3f(0,1,0)
	glBegin(GL_LINES)
	glVertex3f(r,t,0)
	#left top when dir=1, righ bottom when dir = =-1
	glVertex(i.dir*l,i.dir*t,0)
	glEnd()

	#green line 2
	#based in bottom left
	glBegin(GL_LINES)
	glVertex3f(l,b,0)
	glVertex3f(i.dir*r,i.dir*b,0)
	glEnd()

	glColor3f(0,0,0)
	glWindowPos3f(winX/2-5,winY/2-5,0)
	glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18,ord(str(i.tmrm)))




def doAnimationStep():
	global Intersections
	i= Intersections[0]
	global dur
	current_time = int(time())
	if dur!=(current_time-init_time):
		dur= current_time-init_time
		i.tmrm -=1
		if i.tmrm==-1:
			if i.dir>0:
				i.tmrm=i1.tm_x
			else:
				i.tmrm=i1.tm_y
			i.dir= -i.dir

	
	sleep(1/float(frameRate))
	glutPostRedisplay()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	#draw intersection rectangles
	for i in Intersections:
		displayIntersection(i)


	glutSwapBuffers()

frameRate = 20
init_time = int(time())
dur = 0

#initialize set of intersections
Intersections =[]
Intersections.append(Intersection(50,50))


#initialize the window
def init():
	glClearColor(0.5,0.5,0.5,1)
	glShadeModel(GL_SMOOTH)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(winX,winY)

glutCreateWindow(sys.argv[0])
init()
glutDisplayFunc(display)
glutIdleFunc(doAnimationStep)
glutMainLoop()







