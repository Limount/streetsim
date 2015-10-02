

def drawFilledCircle(x, y, radius):
	triangleAmount = 10
	tau = 2.0 * np.pi
	print 'hey'
	glBegin(GL_TRIANGLE_FAN)
	glVertex2f(x, y)
	for i in range(triangleAmount):
			glVertex2f(x + (radius * np.cos(i *  tau / triangleAmount)),y + (radius * np.sin(i * tau / triangleAmount)))
	glEnd()



def displayIntersection(i):
	#define the corners of the intersection using the xy coordinates and
	#the height and width of the intersction
	#x,y are the coordinates of the center of the intersection
	#l,r,t,b are the corners of the intersection  
	x=i.x/(winX/2)-1
	y=i.y/(winY/2)-1
	r = i.wd/2/winX
	l = -r 
	t = i.ht/2/winY
	b = -t



	glColor3f(1,1,1)
	glBegin(GL_QUADS)
	glVertex3f(r+x,t+y,0)
	glVertex3f(r+x,b+y,0)
	glVertex3f(l+x,b+y,0)
	glVertex3f(l+x,t+y,0)
	glEnd()

	if i.dir>0:
		glColor3f(1,0,0)
	else:
		glColor3f(0,1,0)

	drawFilledCircle(x,y+t,5)
	drawFilledCircle(x,y+b,5)

	if i.dir>0:
		glColor3f(0,1,0)
	else:
		glColor3f(1,0,0)
	drawFilledCircle(x+r,y,5)
	drawFilledCircle(x+l,y,5)

	#draw lines indicating intesection direction
	glColor3f(1,0,0)
	#red line1 (flips when intersection flips)
	#based in upper left
	glBegin(GL_LINES)
	glVertex3f(l+x,t+y,0)
	#this point moves to opposite corner when the light switches
	#at lower left when dir=0, upper right while dir=1
	glVertex3f(i.dir*l+x,i.dir*b+y,0)
   	glEnd()

	#redline2
	#based in lower right
	glBegin(GL_LINES)
	glVertex3f(r+x,b+y,0)
	#this point moves to opposite corner when the light switches
	glVertex3f(i.dir*r+x,i.dir*t+y,0)
	glEnd()
	
	#green line 1
	#based in upper right
	glColor3f(0,1,0)
	glBegin(GL_LINES)
	glVertex3f(r+x,t+y,0)
	#left top when dir=1, righ bottom when dir = =-1
	glVertex(i.dir*l+x,i.dir*t+y,0)
	glEnd()

	#green line 2
	#based in bottom left
	glBegin(GL_LINES)
	glVertex3f(l+x,b+y,0)
	glVertex3f(i.dir*r+x,i.dir*b+y,0)
	glEnd()

	glColor3f(0,0,0)
	glWindowPos3f(i.x-7,i.y-5,0)
	for c in str(i.tmrm):
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12,ord(c))

