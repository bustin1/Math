import pyglet
from pyglet.gl import *
from pyglet import clock
import numpy as np

WIDTH = 800
HEIGHT = 600

scale = 30 # amplitude
inc = .01 # period
n = 256 # number of gradient vectors


class Noise:
    def __init__(self):
        self.gradient = []
        for i in range(n):
            self.gradient.append(np.random.rand() * 2 - 1)

    def lerp(self, x1, x2, t):
        y1 = self.gradient[x1]
        y2 = self.gradient[x2]
        return (1-t)*y1 + t*y2

    def smooth(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def noise(self, x):
        xmin = int(x)
        t = self.smooth(x % 1.0)
        xmax = xmin + 1

        return self.lerp(xmin & (n-1), xmax & (n-1), t)



class myWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.noise = Noise()
        self.origin_x = 0
        self.origin_y = HEIGHT/2

    def on_draw(self):
        self.update()

    def octave(self, freq, amp):
        window.clear()
        xoff = 0

        points = [] # only y-coordinate
        for x in range(WIDTH):
            points.append(scale * amp * self.noise.noise(xoff))
            xoff += freq

        return points

    def pairWiseSum(self, a, b):
        length = len(a)
        assert(len(a) == len(b))
        new = []
        for i in range(length):
            new.append(a[i] + b[i])
        return new


    def update(self):

        points = [0 for i in range(WIDTH)]
        for i in range(5): # change this parameter to add more ocatves
            # known as pink noise, when freq and amplitude are inversely
            # proportional. This is also known as a fractal sum.
            points = self.pairWiseSum(self.octave(.1 * i, 1/i), points)

        glBegin(GL_LINE_STRIP)
        for x in range(WIDTH):
            glVertex2f(self.origin_x + x, self.origin_y + points[x])
        glEnd()



if __name__ == "__main__":
    window = myWindow(width=WIDTH, height=HEIGHT)
    window.set_caption("Perlin Noise")
#    clock.schedule_interval(window.update, 1/60) # custom updates
    pyglet.app.run() # enter application event loop



