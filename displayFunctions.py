from OpenGL.GLUT import *
from OpenGL.GL import *
import numpy as np
from globalvars import WIN_Y,WIN_X,FRAME_RATE,INT_ID
from classdefs import *
from time import sleep


# gl wants us to give verteces in the range [-1,1] where 0,0 is the center of the window.
# to keep us a little more sane, we keep the dimensions in a [0,WIN_X],[0,winY] ranges and transform them here
def vertex(x, y):
    glVertex3f(float(x) / (WIN_X / 2) - 1, float(y) / (WIN_Y/ 2) - 1, 0)


def drawFilledCircle(x, y, radius=3.0):
    # there's no simple way to draw a circle in GLUT, so you draw a bunch of isosolece triangles that share the same center point
    triangleAmount = 10
    tau = 2.0 * np.pi
    glBegin(GL_TRIANGLE_FAN)
    vertex(x, y)
    for i in range(triangleAmount + 1):
        vertex(x + (radius * np.cos(i * tau / triangleAmount)), y + (radius * np.sin(i * tau / triangleAmount)))
    glEnd()


def displayIntersection(i, neighbors):
    edge_ct = len(neighbors)
    # draw the white background of the intersection
    glColor3f(1, 1, 1)

    #the intersection consists of edges perpendicular to the connected roads i.width distance from the the centerpoint

    # draw the top and bottom circles.
    # switch color between red and green depending on the the current state of dir in the intersection class
    if i.dir > 0:
        glColor3f(1, 0, 0)
    else:
        glColor3f(0, 1, 0)

    drawFilledCircle(i.x, i.nw.y)
    drawFilledCircle(i.x, i.se.y)

    if i.dir > 0:
        glColor3f(0, 1, 0)
    else:
        glColor3f(1, 0, 0)
    drawFilledCircle(i.nw.x, i.y)
    drawFilledCircle(i.se.x, i.y)

    glColor3f(0, 0, 0)
    glWindowPos3f(i.x - 7, i.y - 5, 0)
    for c in str(i.tmrm):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))


def displayDashedLine(a,b, dashLength=10.0, dashGap=5.0):

    point_dx = b.x-a.x
    point_dy = b.y-a.y

    if b.x == a.x:
        # length of each dash in the x direction
        dx_d = 0
        # length of each dash in the y direction
        dy_d = dashLength
        # length between the beginning of one dash to the beginning of the next dash in the x direction
        dx_t = 0
        # length between the beginning of one dash to the beginning of the next dash in the y direction
        dy_t = dashLength + dashGap
    else:
        dx_d = dashLength / np.sqrt(1+(point_dy/point_dx)**2)
        #a little mathematical oddity. We lose our important negative sign in the squaring
        if point_dx<0:
            dx_d = -dx_d
        dy_d = (point_dy/point_dx)*dx_d

        dx_t = (dashLength+dashGap) / np.sqrt(1+(point_dy/point_dx)**2)
        if point_dx<0:
            dx_t = -dx_t
        dy_t = (point_dy/point_dx)*dx_t

    # we draw the dashed line by finding the slope between the two points
    # and then iteratively drawing a set of line segments between those two points


    # find the number of full dashes to be drawn
    totalLineDistance = np.sqrt((point_dx) ** 2 + (point_dy) ** 2)
    dashCount = int(totalLineDistance / (dashLength + dashGap))
    # draw the dashes using x,y as the the moving start point and x+dx_d,y+dx_y as the end points
    x = a.x
    y = a.y
    for i in range(dashCount):
        glBegin(GL_LINES)
        vertex(x, y)
        vertex(x + dx_d, y + dy_d)
        glEnd()
        x += dx_t
        y += dy_t
    # the final dash truncates at the end point if there is not space for a full line
    if totalLineDistance / (dashLength + dashGap) - dashCount > (dashLength / (dashLength + dashGap)):
        glBegin(GL_LINES)
        vertex(x, y)
        vertex(x + dx_d, y + dy_d)
        glEnd()
    else:
        glBegin(GL_LINES)
        vertex(x, y)
        vertex(b.x, b.y)
        glEnd()


def displayRoad(i1, i2, width = 10):
    if (i1.x < i2.x) or (i1.x == i2.x and i1.y < i2.y):
        a = Point(i1.x,i1.y)
        b = Point(i2.x,i2.y)
    else:
        a = Point(i2.x,i2.y)
        b = Point(i1.x,i1.y)
    glColor3f(0.5, 0.25, 0)
    print 'a',a.x,a.y
    print 'b',b.x,b.y
    if a.x==b.x:
        dx = width
        dy = 0
    else:

        slope = (b.y-a.y)/(b.x-a.x)
        t1 = np.arctan(slope)
        t2 = np.pi/2 - t1
        dx = width*np.sin(t1)
        dy = width*np.sin(t2)

    glBegin(GL_QUADS)
    vertex(a.x-dx, a.y+dy)
    vertex(a.x+dx, a.y-dy)
    vertex(b.x+dx, b.y-dy)
    vertex(b.x-dx, b.y+dy)
    glEnd()
    glColor3f(1, 1, 0)
    displayDashedLine(a, b)

def displayRoads(map):
    i = 0
    for road in map.edges_iter():
        i += 1
        displayRoad(road[0],road[1])


def displayVehicles(Vehicles):
    for v in Vehicles:
        glColor3f(0, 0, 1)
        glBegin(GL_QUADS)
        vertex(v.x + 8, v.y + 8)
        vertex(v.x + 8, v.y - 8)
        vertex(v.x - 8, v.y - 8)
        vertex(v.x - 8, v.y + 8)
        glEnd()
