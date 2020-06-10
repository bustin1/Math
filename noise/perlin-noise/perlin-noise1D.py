import pyglet
import numpy as np
from pyglet.gl import *
from pyglet import *

WIDTH = 800
HEIGHT = 600
n = 256 # must be a power of 2 for the noise functino to work

freq = .01
amp = 100

# Note that gradients are
# uniformly distributed by a rectangle
# not a circle. Go to scratch pixel and 
# part 2 of perlin noise to learn
# more about how to distribute over a circle
class Noise:
    def __init__(self):
        self.gradient = []
        for i in range(n):
            y = 2 * np.random.rand() - 1
            self.gradient.append(y)


    def smooth(self, t):
        return t * t * t * (t * (6*t - 15) + 10)

    def lerp(self, x1, x2, t):
        return (1-t)*x1 + t*x2

    def hash(self, x, y):
        return self.permTab[self.permTab[x] + y]

    def noise(self, x):
        lo = int(np.floor(x)) & (n-1)
        xt = x % 1.0
        hi = (lo + 1) & (n-1)

        s0 = self.gradient[lo]
        s1 = self.gradient[hi]

        x0 = s0 * xt
        x1 = -s1 * (1 - xt)

        xt = self.smooth(xt)

        return self.lerp(x0, x1, xt)


class myWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.noise = Noise()
        self.origin_x = 0
        self.origin_y = HEIGHT/2

    def on_draw(self):
        window.clear()
        self.update()

    def on_mouse_press(self, x, y, buttons, modifier):
        print("(%d, %d)"%(x,y))

    def octave(self, num):


        glBegin(GL_POINTS)
        for x in range(WIDTH):

            y = 0
            acc = 1

            for i in range(num):
                f = freq * acc
                a = amp / acc
                y += a * (self.noise.noise(x * f))
                acc *= 2

            glVertex2f(self.origin_x + x, self.origin_y + y)

        glEnd()

    def update(self):

        self.octave(5)

        print("updated.")


if __name__ == "__main__":
    window = myWindow(width=WIDTH, height=HEIGHT)
    pyglet.app.run()









