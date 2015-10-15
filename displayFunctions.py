from OpenGL.GLUT import *
from OpenGL.GL import *
import numpy as np
from globalvars import winY, winX, frameRate
from classdefs import *
from time import sleep


# gl wants us to give verteces in the range [-1,1] where 0,0 is the center of the window.
# to keep us a little more sane, we keep the dimensions in a [0,winX],[0,winY] ranges and transform them here
def vertex(x, y):
    glVertex3f(float(x) / (winX / 2) - 1, float(y) / (winY / 2) - 1, 0)


def drawFilledCircle(x, y, radius=3.0):
    # there's no simple way to draw a circle in GLUT, so you draw a bunch of isosolece triangles that share the same center point
    triangleAmount = 10
    tau = 2.0 * np.pi
    glBegin(GL_TRIANGLE_FAN)
    vertex(x, y)
    for i in range(triangleAmount + 1):
        vertex(x + (radius * np.cos(i * tau / triangleAmount)), y + (radius * np.sin(i * tau / triangleAmount)))
    glEnd()


def displayIntersection(i):
    # draw the white background of the intersection
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    vertex(i.ne.x, i.ne.y)
    vertex(i.se.x, i.se.y)
    vertex(i.sw.x, i.sw.y)
    vertex(i.nw.x, i.nw.y)
    glEnd()

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


def displayDashedLine(a, b, dashLength=10.0, dashGap=5.0):
    # we draw the dashed line by finding the slope between the two points
    # and then iteratively drawing a set of line segments between those two points

    # cant calculate slope when the points are vertical
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
        slope = (b.y - a.y) / (b.x - a.x)
        dx_d = np.sqrt((dashLength ** 2) / 1 + (slope ** 2))
        dy_d = slope * dx_d
        dx_t = dx_d + np.sqrt((dashGap ** 2) / 1 + (slope ** 2))
        dy_t = dy_d + slope * dx_d
    # find the number of full dashes to be drawin
    totalLineDistance = np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
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


# At this point I am try to keep this such that roads to not need to be perfectly all right angles
def displayRoadHorizontal(i1, i2):
    glColor3f(0.5, 0.25, 0)
    glBegin(GL_QUADS)
    vertex(i1.ne.x, i1.ne.y)
    vertex(i2.nw.x, i2.nw.y)
    vertex(i2.sw.x, i2.sw.y)
    vertex(i1.se.x, i1.se.y)
    glEnd()

    # display the center dashed line
    # note that we don't give the translated points
    a = Corner((i1.ne.x + i1.se.x) / 2, (i1.ne.y + i1.se.y) / 2)
    b = Corner((i2.nw.x + i2.sw.x) / 2, (i2.nw.y + i2.sw.y) / 2)

    glColor3f(1, 1, 0)
    displayDashedLine(a, b)


def displayRoadVertical(i1, i2):
    glColor3f(0.5, 0.25, 0)
    glBegin(GL_QUADS)
    vertex(i1.ne.x, i1.ne.y)
    vertex(i2.se.x, i2.se.y)
    vertex(i2.sw.x, i2.sw.y)
    vertex(i1.nw.x, i1.nw.y)
    glEnd()

    a = Corner((i1.nw.x + i1.ne.x) / 2, (i1.nw.y + i1.ne.y) / 2)
    b = Corner((i2.sw.x + i2.se.x) / 2, (i2.sw.y + i2.se.y) / 2)

    glColor3f(1, 1, 0)
    displayDashedLine(a, b)


def displayRoads(Intersections):
    # displayRoadVertical(Intersections[2][3],Intersections[3][3])
    for i in range(1, len(Intersections[0])):
        for j in range(0, len(Intersections)):
            displayRoadVertical(Intersections[i - 1][j], Intersections[i][j])
            #
    for i in range(0, len(Intersections[0])):
        for j in range(1, len(Intersections)):
            displayRoadHorizontal(Intersections[i][j - 1], Intersections[i][j])


def displayVehicles(Vehicles):
    for v in Vehicles:
        print v.y, v.x
        glColor3f(0, 0, 1)
        glBegin(GL_QUADS)
        vertex(v.x + 8, v.y + 8)
        vertex(v.x + 8, v.y - 8)
        vertex(v.x - 8, v.y - 8)
        vertex(v.x - 8, v.y + 8)
        glEnd()
