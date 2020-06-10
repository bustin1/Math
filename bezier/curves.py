import pyglet
import numpy as np
from pyglet.gl import *
from cpts import Cpts, Cpt

WIDTH = 600
HEIGHT = 600


class myWindow(pyglet.window.Window):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        glClearColor(.5, .5, .5, 1)
        self.vList = []

        # intial control points
        self.copts = Cpts(Cpt(100, HEIGHT/2), Cpt(WIDTH-100, HEIGHT/2))

        # flag the stages of dragging
        self.dragging = 0

        self.ptInd = 0
        self.ball = [0, 0]
        self.x = 0
        self.draw()


    def on_draw(self):
        self.clear()
        glColor3f(0, 0, 0)

        pyglet.graphics.draw(len(self.copts), GL_LINE_STRIP, ('v2f',
                                                              self.copts.format()))
        pyglet.graphics.draw(len(self.vList)//2,
                             GL_LINE_STRIP, ('v2f', self.vList))
        pyglet.graphics.draw(len(self.copts.circle(
            *self.ball))//2, GL_LINE_STRIP, ('v2f', (self.copts.circle(*self.ball))))

    def __call__(self, dt):

        self.ball = []
        self.lerp(self.x, self.copts.toList(), self.ball)
        self.on_draw()
        self.x += .01
        if self.x > 1:
            pyglet.clock.unschedule(self)
            self.x = 0

    def on_mouse_press(self, x, y, button, modifiers):

        if pyglet.window.mouse.RIGHT & button:
            self.copts.add(x, y)
        else:
            for i, pt in enumerate(self.copts.toList()):
                if (pt[0]-x)**2 + (pt[1]-y)**2 < 100:
                    self.dragging = 1
                    self.ptInd = i

    def on_mouse_drag(self, x, y, dx, dy, button, modifers):

        if self.dragging >= 1:
            self.copts.toList()[self.ptInd] = (x, y)
            self.vList = []
            self.draw()
            self.dragging = 2

    def on_mouse_release(self, x, y, buttons, modifers):
        if self.dragging == 2:
            pyglet.clock.schedule_interval(self, .05)
            self.dragging = 0
            self.ptInd = 0

    def draw(self):
        for i in range(101):
            self.lerp(i/100, self.copts.toList(), self.vList)
        self.on_draw()

    def lerp(self, x, copts, L):

        l = len(copts) - 1

        if l <= 0:
            x, y = copts[0]
            L.extend([x, y])
            return

        pts = []

        for i in range(l):
            pts.append(self.propDist(copts[i], copts[i+1], x))

        self.lerp(x, pts, L)


    def propDist(self, pt1, pt2, x):
        pt = (pt1[0] + x*(pt2[0] - pt1[0]), pt1[1] + x*(pt2[1] - pt1[1]))
        return pt


if __name__ == "__main__":
    window = myWindow(width=WIDTH, height=HEIGHT)
    pyglet.app.run()

# TODO: possibly add generator object to lerp
# mouse drag control points
# add control points
# instanenous draw, then draw circle

