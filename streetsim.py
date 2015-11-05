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
from globalvars import WIN_X,WIN_Y,FRAME_RATE
import networkx as nx

## some API in the chain is translating the keystrokes to this octal string
# so instead of saying ESCAPE=27, we use the following
#   -from the pyopengl demo files
ESCAPE = '\033'

#this function is run continuously, as specified by glutIdleFunc
def doAnimationStep():
    global Intersections
    global dur
    #current time with a one second precision
    current_time = int(time())
    #the following IF will be run once every second.
    if dur != (current_time - init_time):
        dur = current_time - init_time
        #iterate through each intersection in the network to see which lights need to be switched
        # for street in Intersections:
        #     for i in street:
        #         i.tmrm -= 1
        #         if i.tmrm == -1:
        #             if i.dir > 0:
        #                 i.tmrm = i.tm_x
        #             else:
        #                 i.tmrm = i.tm_y
        #             i.dir = -i.dir
        for v in Vehicles:
            v.y+=v.speed
    #sleep pauses the program the given number of seconds. Waiting 1/frameRate means doAnimationStep will run roughly frameRate times a second (slightly lower for processing time)
    sleep(1 / float(FRAME_RATE))
    glutPostRedisplay()


def display():
    #GL related stuff that I dont really understand
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #load in the global window dimensions
    global WIN_X,WIN_Y
    #Output all the roads, using the intersections to deduce where the roads are
    displayRoads(map)
    # draw intersection rectangles
    # GOING TO WAIT ON THIS, GET ROADS FIRST
    # for street in Intersections:
    #     for i in street:
    #         displayIntersection(i)

    displayVehicles(Vehicles)
    #more GL related stuff i dont really understad
    glutSwapBuffers()

def add_network_attributes(map):
    # first we add the lengths of the road to each edge
    # and the angle of each road from each intersection
    for i1 in map.nodes_iter():
        x1 = float(i1.x)
        y1 = float(i1.y)
        for i2 in map.neighbors(i1):
            x2 = float(i2.x)
            y2 = float(i2.y)

            map[i1][i2]['distance']= np.sqrt((x1-x2)**2 + (y1-y2)**2)
            # calculating the angle is oddly difficult. Maybe I'm missing a simple method
            if x1 == x2 and y2>y1:
                map[i1][i2]['angle'] = np.pi/2
            if x1 == x2 and y2<y1:
                map[i1][i2]['angle'] = -np.pi/2
            if x2>x1 and y2>=y1:
                map[i1][i2]['angle'] = np.arctan((y2-y1)/(x2-x1))
            if x2>x1 and y2<y1:
                map[i1][i2]['angle'] = np.arctan((y2-y1)/(x2-x1)) + np.pi*2
            if x2<x1:
                map[i1][i2]['angle'] = np.arctan((y2-y1)/(x2-x1)) + np.pi

        # now I want to match up through ways. ie, when going straight, which road goes to which road

        #create a list of the angles of each intersection, sorted
        angles = []
        for i2 in map.neighbors(i1):
            angles.append(map[i1][i2]['angle'])
        angles.sort()
        #verify that the roads aren't too close too each other
        for i in range(len(angles)-1):
            if angles[i+1]-angles[i]<(np.pi/6):
                print 'Intersections at ',i1.x,i1.y
                print 'Angles ',angles[i+1],angles[i]
                raise ValueError('One of your intersections has an angle that is too small')


        #using the sorted angles we're going to create a list of the interesections sorted by angle
        #note that is this legal because we have already proved that all the angles are distinct
        ints_by_angle = []
        for i2 in map.neighbors(i1):
            for i in range(len(angles)):
                if map[i1][i2]['angle']==angles[i]:
                    ints_by_angle.append(i2)

        print len(angles) == len(ints_by_angle)

        map.node[i1]['cnx']=[None,None]
        if len(angles)==1:
            map.node[i1]['cnx'][0] = ints_by_angle[0]
        elif len(angles)==2:
            #if the angle between the roads are between 2pi/3 and 4pi/3 then it is a str8 road with lighted crosswalk
            #else they take turns going through the intersection
            if 2*np.pi/3 < (angles[1]-angles[0]) < 4*np.pi/3:
                map.node[i1]['cnx'][0] = [ints_by_angle[0],ints_by_angle[1]]
            else:
                map.node[i1]['cnx'][0] = ints_by_angle[0]
                map.node[i1]['cnx'][1] = ints_by_angle[1]

        elif len(angles)==3:
            #when there are three in an intersection, the two that have the greatest angle between them become connected
            if ((angles[1]-angles[0]) >= (angles[2]-angles[1]) >= (2*np.pi + (angles[0]-angles[2]))):
                map.node[i1]['cnx'][0] = [ints_by_angle[0],ints_by_angle[1]]
                map.node[i1]['cnx'][1] = ints_by_angle[2]
            elif ((angles[2]-angles[1]) >= (2*np.pi + (angles[0]-angles[2])) >= (angles[1]-angles[0])):
                map.node[i1]['cnx'][0] = [ints_by_angle[1],ints_by_angle[2]]
                map.node[i1]['cnx'][1] = ints_by_angle[0]
            else:
                map.node[i1]['cnx'][0] = [ints_by_angle[0],ints_by_angle[2]]
                map.node[i1]['cnx'][1] = ints_by_angle[1]
        elif len(angles)==4:
            map.node[i1]['cnx'][0] = [ints_by_angle[1],ints_by_angle[3]]
            map.node[i1]['cnx'][1] = [ints_by_angle[0],ints_by_angle[2]]
        # an intersection with 1 or >4 neighbors wtf???
        else:
            print 'Angle ct ',len(angles)
            print 'Intersection at ',i1.x,i1.y
            raise ValueError('One of your intersections has >4 roads coming out of it')


    #End add_network_attributes()

init_time = int(time())
dur = 0

# Network = {'a':Intersection(50,50),
#            'b':Intersection(110,50),
#            'c':Intersection(200,80),
#            'd':Intersection(150,150),
#            'e':Intersection(220,150),
#            'f':Intersection(260,40)}

Is = [Intersection(100,100),
      Intersection(220,100),
      Intersection(400,160),
      Intersection(300,300),
      Intersection(440,300),
      Intersection(520,80),
      Intersection(200,50)]
#once you have created your full list of Intersections, then you can add the paths between them.
# this does not feel like ideal programming practice, but I can't figure out the best way to do this


map = nx.Graph()
#add roads that connect the intersections
map.add_edge(Is[0],Is[1])
map.add_edge(Is[1],Is[2])
map.add_edge(Is[1],Is[3])
map.add_edge(Is[2],Is[4])
map.add_edge(Is[2],Is[5])
map.add_edge(Is[3],Is[4])
map.add_edge(Is[4],Is[5])
map.add_edge(Is[6],Is[5])
map.add_edge(Is[6],Is[1])
#give each edge a distance attribute using the coordinates of each intersection
add_network_attributes(map)


Vehicles = [Vehicle(),Vehicle(120,100)]

# initialize the window
def init():
    glClearColor(0.5, 0.5, 0.5, 1)
    glShadeModel(GL_SMOOTH)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIN_X,WIN_Y)

glutCreateWindow(sys.argv[0])
init()
glutDisplayFunc(display)
glutIdleFunc(doAnimationStep)
glutMainLoop()
