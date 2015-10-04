from numpy.random import randint

from globalvars import winX,winY,frameRate

class Corner:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Vehicle:
	def __init__(self,curX=50,curY=50,finalDestX=350,finalDestY=350,speed=1):
		self.x = curX
 		self.y = curY
 		self.nextDestX = curX
 		self.nextDesty = curY
 		self.finalDestX = finalDestX
 		self.finalDestY = finalDestY
 		self.speed = speed
		#wait tolerance = randint(15) once I figure out how to calculate 
		#expected path time
		#right now they will just take the open light
		 			



class Intersection:
	def __init__(self,x,y,tm_x=30,tm_y=30,wd=20,ht=20):
		#important to use integers here and not a list of length two because of the immutable object problem that i dont fully understand
		self.tm_x = tm_x
		self.tm_y = tm_y
		if randint(2):
			self.dir = -1
			self.tmrm = randint(tm_x)
		else:
			self.dir =1
			self.tmrm = randint(tm_y)
		self.init_tm = self.tmrm
		#center of the intersection
		self.x = float(x)
		self.y = float(y)
		self.wd = float(wd)
		self.ht = float(ht)
		#the four corners of the intersections
		self.ne = Corner(self.x+self.wd/2,self.y+self.ht/2)
		self.se = Corner(self.x+self.wd/2,self.y-self.ht/2)
		self.nw = Corner(self.x-self.wd/2,self.y+self.ht/2)
		self.sw = Corner(self.x-self.wd/2,self.y-self.ht/2)
		#the four corners of the intersection recalculated to fit in the normalized window
		self.x_trans = self.x/(winX/2)-1
		self.y_trans = self.y/(winY/2)-1
		self.ne_trans = Corner(self.ne.x/(winX/2)-1,self.ne.y/(winY/2)-1)
		self.se_trans = Corner(self.se.x/(winX/2)-1,self.se.y/(winY/2)-1)
		self.nw_trans = Corner(self.nw.x/(winX/2)-1,self.nw.y/(winY/2)-1)
		self.sw_trans = Corner(self.sw.x/(winX/2)-1,self.sw.y/(winY/2)-1)
		self.init_tm = self.tmrm

