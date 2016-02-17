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
import pandas as pd
import sys
import getopt


## some API in the chain is translating the keystrokes to this octal string
# so instead of saying ESCAPE=27, we use the following
#   -from the pyopengl demo files
ESCAPE = '\033'
SPACEBAR = '\040'

#this function is run continuously, as specified by glutIdleFunc
def doAnimationStep():
    global map
    global dur
    global pause
    #current time with a one second precision
    if not pause:
        current_time = int(time())
        #the following IF will be run once every second.
        if dur != (current_time - init_time):
            dur = current_time - init_time
            #iterate through each intersection in the network to see which lights need to be switched
            # for street in Intersections:
            for i in map.nodes():
                i.tmrm -= 1
                if i.tmrm == -1:
                    # switch the go and stop intersections
                    #map.node[i]['cnx'][0], map.node[i]['cnx'][1] = map.node[i]['cnx'][1], map.node[i]['cnx'][0]
                    if i.dir > 0:
                        i.dir = 0
                    else:
                        i.dir = 1

                    i.tmrm = i.tm[i.dir]
        for v in map.Vehicles:
            # check for red light
            if v.prev_int in map.node[v.next_int]['cnx'][v.next_int.dir]:
                v.incoming_red = 1
            else:
                v.incoming_red = 0

            if v.active:
                v.update()
            else:
                times.append(time() - v.init_time)
                distances.append(v.distance_traveled)
                map.Vehicles.remove(v)

                map.add_vehicle()

        #sleep pauses the program the given number of seconds. Waiting 1/frameRate means doAnimationStep will run roughly frameRate times a second (slightly lower for processing time)
        sleep(1 / float(FRAME_RATE))

        glutPostRedisplay()


def keyPressed(*args):
    global pause
    global init_time
    if args[0] == SPACEBAR:
        pause = not pause
        #TODO the way my timing is set up, the timing gets a little messed up (adding/subtracting a fraction of a second). Not major, but the timing system should be refactored at some point
    if args[0] == ESCAPE:
        d = {'distance': distances, 'time': times}
        results = pd.DataFrame(d)
        print 'Average time: ', results['time'].mean()
        print 'Average speed: ', (results['distance'].mean() / results['time'].mean())
        results.to_csv('results.csv')
        quit()

def display():
    #GL related stuff that I dont really understand
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #load in the global window dimensions
    global WIN_X,WIN_Y
    #Output all the roads, using the intersections to deduce where the roads are
    displayRoads(map)

    displayTrafficLights(map)
    displayVehicles(map)
    #more GL related stuff i dont really understad
    glutSwapBuffers()

def map_from_argfile(argv):
    if 'streetsim.py' in argv[0]:
        argv = argv[1:]
    print argv
    try:
        opts, args = getopt.getopt(argv,'hi:',["mapfile="])
    except getopt.GetoptError:
        print 'streetsim.py -i <mapfile.ssm>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Sorry, good luck'
            sys.exit()
        elif opt in ("-i", "--mapfile"):
            inputfile = arg

        with open('default.ssm', 'r') as f:
            ssm = f.read()
        locationsraw = ssm.split(';\n')[0]
        relationsraw = ssm.split(';\n')[1]
        locations = []
        for l in locationsraw.split('\n'):
            locations.append(l.split(','))
        print locations
        relations = []
        for r in relationsraw.split('\n'):
            relations.append(r.split(','))
        print relations

        map = nx.DiGraph()

        intersections = []
        for i in locations:

            intersections.append(Intersection(int(i[0]),int(i[1])))

        for r in relations:
            map.add_edge(intersections[int(r[0])],intersections[int(r[1])])

        return map




init_time = int(time())
dur = 0
pause = False

#once you have created your full list of Intersections, then you can add the paths between them.
# this does not feel like ideal programming practice, but I can't figure out the best way to do this

def two_way_edge(map,i1,i2):
    map.add_edge(i1,i2)
    map.add_edge(i2,i1)

times = []
distances = []

map = map_from_argfile(sys.argv)

#give each edge a distance attribute using the coordinates of each intersection
map.add_network_attributes()


for i in range(10):
    map.add_vehicle()

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
glutKeyboardFunc(keyPressed)
glutIdleFunc(doAnimationStep)
glutMainLoop()
