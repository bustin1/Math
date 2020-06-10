import pyglet
from pyglet.gl import *
from pyglet import clock
import numpy as np

WIDTH = 512
HEIGHT = 512

scale = 255 # amplitude
n = 256 # number of gradient vectors


class Noise:
    def __init__(self):
        self.gradient = []
        for i in range(n * n):
            self.gradient.append(np.random.rand())

    def lerp(self, x1, x2, t):
        return (1-t)*x1 + t*x2

    def smooth(self, t):
#        return t * t * (3 - 2 * t)
        return t * t * t * (t * (t * 6 - 15) + 10)

    def noise(self, x, y):
        xmin = int(x) % n
        xt = self.smooth(x % 1.0)
        xmax = (xmin + 1) % n

        ymin = int(y) % n
        yt = self.smooth(y % 1.0)
        ymax = (ymin + 1) % n

        n0 = self.lerp(self.gradient[(xmin + ymin * n)],
                self.gradient[(xmax + ymin * n)], xt)
        n1 = self.lerp(self.gradient[(xmin + ymax * n)],
                self.gradient[(xmax + ymax * n)], xt)

        return self.lerp(n0, n1, yt)



class myWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.noise = Noise()
        self.origin_x = 0
        self.origin_y = 0
        self.start = 0

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)

    def on_draw(self):
        window.clear()
        self.update()

    def octave(self, freq, amp):
        window.clear()
        xoff = 0
        yoff = 0

        points = [] # color
        for x in range(WIDTH):
            for y in range(HEIGHT):
                points.append(amp * self.noise.noise(xoff, yoff))
                yoff += freq
            xoff += freq
            yoff = 0

        return points

    def pairWiseSum(self, a, b):
        length = len(a)
        assert(len(a) == len(b))
        new = []
        for i in range(length):
            new.append(a[i] + b[i])
        return new

    def update(self):

        xoff = 0
        yoff = 0

        points = [0 for i in range(WIDTH * HEIGHT)]
        for i in range(5):
            points = self.pairWiseSum(self.octave(.01 * pow(2, i), 1/pow(2,i)), points)

        maxNoiseVal = np.amax(points)
        print(maxNoiseVal)
        points = [i / maxNoiseVal for i in points]

        glBegin(GL_LINE_STRIP)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                c = points[x * HEIGHT + y]
#                c = 10 * c
#                c = c - int(c)
                glColor3f(c, c, c)
                glVertex2f(self.origin_x + x, self.origin_y + y)
        glEnd()

        print("updated.")




if __name__ == "__main__":

    window = myWindow(width=WIDTH, height=HEIGHT, resizable=False)
    window.set_caption("Perlin Noise")
#    clock.schedule_interval(window.update, 1/60) # custom updates
    pyglet.app.run() # enter application event loop



# checkout scratchpixel.com for more information
# all credit should be given to him/her
