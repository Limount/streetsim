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

#add an advanced initialization step after the network has been defined to the NetworkX DiGraph object
def add_network_attributes(self):
    # first we add the lengths of the road to each edge
    # and the angle of each road from each intersection
    for i1 in self.nodes_iter():
        x1 = float(i1.x)
        y1 = float(i1.y)
        for i2 in self.neighbors(i1):
            x2 = float(i2.x)
            y2 = float(i2.y)

            self[i1][i2]['distance']= np.sqrt((x1-x2)**2 + (y1-y2)**2)
            # calculating the angle is oddly difficult. Maybe I'm missing a simple method

            if x1 == x2 and y2>y1:
                self[i1][i2]['angle'] = 0
            if x1 == x2 and y2<y1:
                self[i1][i2]['angle'] = np.pi
            if x2>x1 and y2>=y1:
                self[i1][i2]['angle'] = np.arctan((y2-y1)/(x2-x1))
            if x2>x1 and y2<y1:
                self[i1][i2]['angle'] = np.arctan((y2-y1)/(x2-x1)) + np.pi*2
            if x2<x1:
                self[i1][i2]['angle'] = np.arctan((y2-y1)/(x2-x1)) + np.pi

            #identify the nodes that have a two way street between them
            if i1 in self.neighbors(i2):
                self[i1][i2]['symmetric'] = True
            else:
                self[i1][i2]['symmetric'] = False

        # now I want to match up through ways. ie, when going straight, which road goes to which road

        #create a list of the angles of each intersection, sorted
        angles = []
        for i2 in self.neighbors(i1):
            angles.append(self[i1][i2]['angle'])
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

        for i in range(len(angles)):
            for i2 in self.neighbors(i1):
                if self[i1][i2]['angle']==angles[i]:
                    ints_by_angle.append(i2)

        self.node[i1]['cnx']=[None,None]

        if len(angles)==1:
            self.node[i1]['cnx'][0] = [ints_by_angle[0]]
        elif len(angles)==2:
            #if the angle between the roads are between 2pi/3 and 4pi/3 then it is a str8 road with lighted crosswalk
            #else they take turns going through the intersection
            if 2*np.pi/3 < (angles[1]-angles[0]) < 4*np.pi/3:
                self.node[i1]['cnx'][0] = [ints_by_angle[0],ints_by_angle[1]]
            else:
                self.node[i1]['cnx'][0] = [ints_by_angle[0]]
                self.node[i1]['cnx'][1] = [ints_by_angle[1]]

        elif len(angles)==3:
            #when there are three in an intersection, the two that have the greatest angle between them become connected
            if (angles[1]-angles[0]) >= np.maximum((angles[2]-angles[1]),(2*np.pi + (angles[0]-angles[2]))):
                self.node[i1]['cnx'][0] = [ints_by_angle[0],ints_by_angle[1]]
                self.node[i1]['cnx'][1] = [ints_by_angle[2]]
            elif (angles[2]-angles[1]) >= np.maximum((2*np.pi + (angles[0]-angles[2])),(angles[1]-angles[0])):
                self.node[i1]['cnx'][0] = [ints_by_angle[1],ints_by_angle[2]]
                self.node[i1]['cnx'][1] = [ints_by_angle[0]]
            else:
                self.node[i1]['cnx'][0] = [ints_by_angle[0],ints_by_angle[2]]
                self.node[i1]['cnx'][1] = [ints_by_angle[1]]
        elif len(angles)==4:
            self.node[i1]['cnx'][0] = [ints_by_angle[1],ints_by_angle[3]]
            self.node[i1]['cnx'][1] = [ints_by_angle[0],ints_by_angle[2]]
        # an intersection with 1 or >4 neighbors wtf???
        else:
            print 'Angle ct ',len(angles)
            print 'Intersection at ',i1.x,i1.y
            raise ValueError('One of your intersections has >4 roads coming out of it')

    #End add_network_attributes()

nx.DiGraph.add_network_attributes = add_network_attributes
nx.DiGraph.add_vehicle = add_vehicle
nx.DiGraph.Vehicles = []
