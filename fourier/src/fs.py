import cmath
import random
import math
import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.graphics import Line, Color
from kivy.graphics import SmoothLine
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

Window.size = (800, 600)
w = Window.width//2
h = Window.height//2 
'''
number of vectors - incr for precision
usually set to number of data points 
'''
L = 1031
scale = -3


'''
object to store the functionality
of creating/rotating lines
'''
class myLine:

    def __init__(self):
        self.angle = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.r = 0
        self.freq = 0
        self.line = Line(points=[], width=1)

    def setLength(self, r):
        self.r = r

    def setFreq(self, freq):
        self.freq = 2 * math.pi * freq

    def setPos(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.line.points = [x1,y1,x2,y2]

    def setStartCoor(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def rotateBy(self, time):
        angle = self.freq * time + self.angle
        self.x2 = self.x1 + self.r * math.cos(angle)
        self.y2 = self.y1 + self.r * math.sin(angle)
        self.line.points=[self.x1,self.y1,self.x2,self.y2]

    def setAngle(self, angle):
        self.angle = angle

class myDrawing(Widget):

    def integrate(self, x, y):
        N = len(x)              # number of data points
        coef = []
        i = -(L//2)
        j = L - (L//2)
        for l in range(i, j):
            c = 0
            for t in range(N):
                v = complex(x[t], y[t])
                offset = complex(math.cos(-2*math.pi*l*t/N),
                                 math.sin(-2*math.pi*l*t/N))
                c += v * offset
            c /= N              #dt
            coef.append(c)
        return coef             #array of coefficients in complex numbers

    def update(self, *args):
        for i in range(L):
            self.c[i].rotateBy(self.time)
            if i < L - 1:
                self.c[i+1].setStartCoor(self.c[i].x2, self.c[i].y2)


        #reset after two cycles(1 image every self.time += 1)
        if self.time > 2.05:
            self.time = 0
            self.trace.points = []
        else:
            self.trace.points += [self.c[L-1].x2,self.c[L-1].y2]

        self.time += self.dt


    def __init__(self, **kwargs):
        super(myDrawing, self).__init__(**kwargs)
        with self.canvas:

            #set of data points to draw
            x = []
            y = []

            with open("homer.txt", "r") as f:
                for pos in f:
                    coordinates = pos.split(",")
                    x.append(float(coordinates[0]))
                    y.append(float(coordinates[1]))

            x = [scale * i for i in x]
            y = [scale * i for i in y]
#            x,y = zip(*sorted(zip(x,y)))
            self.time = 0;
            self.dt = 1 / len(x)

            #properties
            self.c = [myLine() for i in range(L)]

            #starting lines
            d = self.integrate(x, y)
            xcurr = 0
            ycurr = 0
            for i in range(L):
                xprev = xcurr
                yprev = ycurr
                xcurr = d[i].real
                ycurr = d[i].imag

                phase = math.atan2(ycurr,xcurr)
                length = math.sqrt(xcurr*xcurr + ycurr*ycurr)
                freq = i - L//2

                self.c[i].setLength(length)
                self.c[i].setFreq(freq)
                self.c[i].setAngle(phase)
                self.c[i].setPos (xprev + w, yprev + h, xcurr + w, ycurr + h)


            Color(0,1,1) # blue
            self.trace = Line(points=[], width=1)

            Clock.schedule_interval(self.update, .001) #update interval

class MyApp(App):

    def build(self):
        return myDrawing()




if __name__ == "__main__":
    MyApp().run()

'''
to draw an image, make sure to use a website to covert svg to
a list of coordinates in the form x,y if you have png or jpeg, 
convert to svg then coordinates. Use this website to convert:
https://shinao.github.io/PathToPoints/
'''









