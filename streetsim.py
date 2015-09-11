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

xloc=-1.0
yloc=-1.0
frameRate = 40
i1 = Intersection(50,50)
init_time = int(time())
dur = 0

def doAnimationStep():
	global xloc
	global yloc
	global i1
	global dur
	print i1.tmrm
	yloc +=1.0/winY
	xloc +=1.0/winX
	current_time = int(time())
	if dur!=(current_time-init_time):
		dur= current_time-init_time
		i1.tmrm -=1
		if i1.tmrm==0:
			if i1.dir>0:
				i1.tmrm=i1.tm_x
			else:
				i1.tmrm=i1.tm_y
			i1.dir= -i1.dir

	
	sleep(1/float(frameRate))
	glutPostRedisplay()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	#draw intersection rectangles
	r = i1.wd/2/winX
	l = -r
	t = i1.ht/2/winY
	b = -t



	glColor3f(1,1,1)
	glBegin(GL_QUADS)
	glVertex3f(r,t,0)
	glVertex3f(r,b,0)
	glVertex3f(l,b,0)
	glVertex3f(l,t,0)
	glEnd()
	#DRAW moving point
	glBegin(GL_POINTS)
	glVertex3f(xloc,yloc,0)
	glEnd()


	#draw lines indicating intesection direction
	glColor3f(1,0,0)
	#red line1 (flips when intersection flips)
	#based in upper left
	glBegin(GL_LINES)
	glVertex3f(l,t,0)
	#this point moves to opposite corner when the light switches
	#at lower left when dir=0, upper right while dir=1
	glVertex3f(i1.dir*l,i1.dir*b,0)
   	glEnd()

	#redline2
	#based in lower right
	glBegin(GL_LINES)
	glVertex3f(r,b,0)
	#this point moves to opposite corner when the light switches
	glVertex3f(i1.dir*r,i1.dir*t,0)
	glEnd()
	

	glutSwapBuffers()



#Define the coordinates of the intersections
inter_coords = np.zeros((5,5,2))
for i in range(0,5):
  for j in range(0,5):
    inter_coords[i][j]=[i,j]
#later we will take a file to import, this is default
map_x = inter_coords.shape[0]
map_y = inter_coords.shape[1]

#print(is_coords)

#define the timing of each light
light_tm = np.zeros((map_x,map_y,2))
for i in range(0,map_x):
  for j in range(0,map_y):
    light_tm[i][j] = [30,30]
#later we will take a file in import, this is default

#print(light_tm)


#randomly define which direction the light allows first and the time remaining
light_init = np.zeros((map_x,map_y,2))
for i in range(0,map_x):
  for j in range(0,map_y):
    light_dir = randint(2)
    light_init[i][j] = [light_dir,randint(light_tm[i][j][light_dir])]

#print(light_init)

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







