from numpy.random import randint, choice
from numpy import sqrt
import globalvars
import networkx as nx
import numpy as np
from time import time

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

    def __init__(self, origin, destination, route, total_distance, max_speed=2):

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
        self.incoming_red = 0

        self.init_time = time()
        self.distance_traveled = total_distance

    def update(self):

        if ( (self.dx>0 and self.dy >=0 and ((self.x+self.dx)>self.next_int.x)) #quadrant 1
        | (self.dx <= 0 and self.dy > 0 and ((self.y+self.dy)>self.next_int.y)) #quandrant 2
        | (self.dx < 0 and self.dy <= 0 and ((self.x+self.dx)<self.next_int.x)) #quandrant 3
        | (self.dx >= 0 and self.dy < 0 and ((self.y+self.dy)<self.next_int.y)) ): #quandrant 4
            if self.incoming_red:
                self.speed = 0
                self.find_vehicle_deltas()
            else:
                self.x = self.next_int.x
                self.y = self.next_int.y
                if self.next_int == self.destination:
                    self.active = 0
                else:
                    if self.speed < self.max_speed: self.speed += 0.05
                    self.prev_int = self.next_int
                    self.road_ct += 1
                    self.next_int = self.route[self.road_ct]
                    self.find_vehicle_deltas()
        else:
            self.x += self.dx
            self.y += self.dy
            if self.speed < self.max_speed:
                self.speed += 0.05
                self.find_vehicle_deltas()


class Intersection:
    def __init__(self, x, y, tm_a=30, tm_b=30, width=15):
        # important to use integers here and not a list of length two because of the immutable object problem that i dont fully understand
        self.tm = [7,5]
        self.dir = randint(2)
        self.tmrm = randint(self.tm[self.dir])
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
    total_distance = 0
    for i in range(len(route)-1):
        total_distance += self[route[i]][route[i+1]]['distance']
    self.Vehicles.append(Vehicle(origin,destination,route,total_distance))

    print 'from ', origin.id, ' to ', destination.id
    r_id = []
    for i in route:
        r_id.append(i.id)
    print 'route: ',r_id


nx.DiGraph.add_vehicle = add_vehicle
nx.DiGraph.Vehicles = []
