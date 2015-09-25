import numpy as np
from numpy.random import randint
import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from time import sleep
from time import time
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
	def __init__(self,curX=50,curY=50,finalDestX=350,finalDestY=350,speed=1):
		self.curX = curX
 		self.curY = curY
 		self.nextDestX = curX
 		self.nextDesty = curY
 		self.finalDestX = finalDestX
 		self.finalDestY = finalDestY
 		self.speed = speed
		#wait tolerance = randint(15) once I figure out how to calculate 
		#expected path time
		#right now they will just take the open light
		 			



class Intersection:
	def __init__(self,x,y,tm_x=30,tm_y=30,wd=40,ht=40,):
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

