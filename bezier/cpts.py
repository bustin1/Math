from dataclasses import dataclass


@dataclass()
class Cpt:
    ''' Class for points '''
    x: float
    y: float


class Cpts:
    def __init__(self, *args):
        self.copts = []
        for pt in args:
            self.copts.append((pt.x, pt.y))

        self.points = []
        for pt in args:
            self.points.extend([pt.x, pt.y])

    def __len__(self):
        return len(self.copts)

    def toList(self):
        return self.copts

    def format(self):
        self.points = []
        for pt in self.copts:
            self.points.extend([*pt])
        return self.points

    # EQ: x^2 + y*2 = 25
    def circle(self, x, y):
        L = []
        for i in range(-5, 6, 1):
            L.extend([x+i, y+(25-i**2)**(.5)])
        for i in reversed(range(-5, 6, 1)):
            L.extend([x+i, y-(25-i**2)**(.5)])

        return L

    def add(self, x, y):
        self.copts.append((x, y))
        self.points.extend([x, y])
