from numpy.random import randint, choice
from numpy import sqrt
import globalvars
import networkx as nx
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vehicle:

    def find_vehicle_deltas(self):
        self.dx = self.speed / np.sqrt(1+((self.next_int.y-self.prev_int.y)/(self.next_int.x-self.prev_int.x))**2)
        #a little mathematical oddity. We lose our important negative sign in the squaring
        if self.next_int.x < self.prev_int.x:
           self.dx = -self.dx
        self.dy = (self.next_int.y-self.prev_int.y)/(self.next_int.x-self.prev_int.x)*self.dx

    def __init__(self, origin, destination, route, max_speed=2):

        self.origin = origin
        self.destination = destination
        self.route = route
        self.prev_int = origin
        self.next_int = route[1]
        self.road_ct = 1
        self.max_speed = max_speed
        self.speed = 0
        self.active = 1
        self.x = origin.x
        self.y = origin.y

        self.find_vehicle_deltas()

    def update(self):

        if ( (self.dx>0 and self.dy >=0 and ((self.x+self.dx)>self.next_int.x)) #quadrant 1
        | (self.dx <= 0 and self.dy > 0 and ((self.y+self.dy)>self.next_int.y)) #quandrant 2
        | (self.dx < 0 and self.dy <= 0 and ((self.x+self.dx)<self.next_int.x)) #quandrant 3
        | (self.dx >= 0 and self.dy < 0 and ((self.y+self.dy)<self.next_int.y)) ): #quandrant 4
            print "BING!"
            self.x = self.next_int.x
            self.y = self.next_int.y
            if self.next_int == self.destination:
                self.active = 0
            else:
                self.prev_int = self.next_int
                self.road_ct += 1
                self.next_int = self.route[self.road_ct]
                self.find_vehicle_deltas()
        else:

            self.x += self.dx
            self.y += self.dy


# A network accepts objects with an x and y variable. Upon initialization, we check to make sure the graph is legal
# legal means: each intersection has 2,3 or 4 connections to other intersections. and the distance between each intersection
# is at least 80 (for now)

# Network receives a list of pairs of intersections upon initialization
class Network:
    def __init__(self, connections):
        # asserting the validity of the received data
        for connection in connections:
            if len(connection) != 2:
                raise ValueError('Network initialization only accepts pairs of intersections')
            for i in range(1):
                if type(connection[i]) is not Intersection:
                    raise TypeError('Network initialization did not receive vertex of type Intersection')
                    # TODO: check for legal graph dimensions


class Intersection:
    def __init__(self, x, y, tm_x=30, tm_y=30, width=15):
        # important to use integers here and not a list of length two because of the immutable object problem that i dont fully understand
        self.tm_x = tm_x
        self.tm_y = tm_y
        if randint(2):
            self.dir = -1
            self.tmrm = randint(tm_x)
        else:
            self.dir = 1
            self.tmrm = randint(tm_y)
        self.init_tm = self.tmrm
        # center of the intersection
        self.x = float(x)
        self.y = float(y)
        self.width = width

        self.id = globalvars.INT_ID
        globalvars.INT_ID += 1


# Add vehicle attributes to the NetworkX.Graph class
def add_vehicle(self, origin=None, destination=None):

    if origin is None:
        origin = choice([x for x in self.nodes() if x !=destination])
    if destination is None:
        destination = choice([x for x in self.nodes() if x !=origin])
    route = nx.dijkstra_path(self,origin,destination,'distance')
    self.Vehicles.append(Vehicle(origin,destination,route))

    print origin.id, origin.x, origin.y
    print destination.id, destination.x,destination.y
    print 'route:'
    for v in route:
        print v.id, v.x,v.y


nx.DiGraph.add_vehicle = add_vehicle
nx.DiGraph.Vehicles = []
