import pyglet
import numpy as np
from pyglet.gl import *
from pyglet import *

WIDTH = 300
HEIGHT = 300
n = 256 # must be a power of 2 for the noise functino to work

freq = .05
amp = 1

# Note that gradients are
# uniformly distributed by a rectangle
# not a circle. Go to scratch pixel and 
# part 2 of perlin noise to learn
# more about how to distribute over a circle
class Noise:
    def __init__(self):
        self.gradient = []
        self.permTab = []
        for i in range(n):
            x = 2 * np.random.rand() - 1
            y = 2 * np.random.rand() - 1
            self.gradient.append([x, y] / np.linalg.norm([x, y]))
            self.permTab.append(i)

        for i in range(n):
            self.swap(self.permTab, i, np.random.randint(n))

        self.permTab += self.permTab

#        print("Table is {0}".format(self.permTab))
#        print("Gradients are {0}".format(self.gradient))

    def swap(self, L, i, j):
        L[i], L[j] = L[j], L[i]

    def smooth(self, t):
        return t * t * t * (t * (6*t - 15) + 10)

    def lerp(self, x1, x2, t):
        return (1-t)*x1 + t*x2

    def hash(self, x, y):
        return self.permTab[self.permTab[x] + y]

    def noise(self, x, y):
        x0 = int(np.floor(x)) & (n-1)
        xt = x % 1.0
        x1 = (x0 + 1) & (n-1)

        y0 = int(np.floor(y)) & (n-1)
        yt = y % 1.0
        y1 = (y0 + 1) & (n-1)

        v00 = [xt, yt]
        v10 = [xt - 1, yt]

        v01 = [xt, yt - 1]
        v11 = [xt - 1, yt - 1]


        c00 = np.dot(v00, self.gradient[self.hash(x0, y0)])
        c10 = np.dot(v10, self.gradient[self.hash(x1, y0)])
        c01 = np.dot(v01, self.gradient[self.hash(x0, y1)])
        c11 = np.dot(v11, self.gradient[self.hash(x1, y1)])

        xt = self.smooth(xt)
        yt = self.smooth(yt)

        n0 = self.lerp(c00, c10, xt)
        n1 = self.lerp(c01, c11, xt)

        return self.lerp(n0, n1, yt)


class myWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.noise = Noise()

    def on_draw(self):
        window.clear()
        self.update()

    def on_mouse_press(self, x, y, buttons, modifier):
        print("(%d, %d)"%(x,y))

    def octave(self, num):


        glBegin(GL_POINTS)
        for x in range(WIDTH):
            for y in range(HEIGHT):

                c = 0
                acc = 1
                maxNoiseVal = 0

                for i in range(num):
                    f = freq * acc
                    a = amp / acc
                    c += a * (self.noise.noise(x * f, y * f) + 1) / 2
                    acc *= 2
                    maxNoiseVal += a

                c = 10 * c
                c = c - int(c)
                glColor3f(c / maxNoiseVal , c / maxNoiseVal, c / maxNoiseVal)
                glVertex2f(x, y)

        glEnd()

    def update(self):

        self.octave(1)

        print("updated.")


if __name__ == "__main__":
    window = myWindow(width=WIDTH, height=HEIGHT)
    pyglet.app.run()









