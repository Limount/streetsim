from numpy.random import randint
from numpy import sqrt
from globalvars import WIN_X,WIN_Y,FRAME_RATE

class Point:
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
		 			
# A network accepts objects with an x and y variable. Upon initialization, we check to make sure the graph is legal
# legal means: each intersection has 2,3 or 4 connections to other intersections. and the distance between each intersection
# is at least 80 (for now)

# Network receives a list of pairs of intersections upon initialization
class Network:
    def __init__(self,connections):
        # asserting the validity of the received data
        for connection in connections:
            if len(connection)!=2:
                raise ValueError('Network initialization only accepts pairs of intersections')
            for i in range(1):
                if type(connection[i]) is not Intersection:
                    raise TypeError('Network initialization did not receive vertex of type Intersection')
        #TODO: check for legal graph dimensions




class Intersection:
    def __init__(self,x,y,tm_x=30,tm_y=30, width=15):
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
        self.width = width


