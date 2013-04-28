# -*- encoding: utf-8 -*-

import math


class Vector(object):
    '''
    immutable class representing three-dimensional vectors
    '''

    def __init__(self, x, y=0, z=0):
        '''
        Constructor
        '''
        if isinstance(x, (list, tuple)):
            coordinates = tuple(x)
        else:
            coordinates = (x, y, z)
        self.coordinates = tuple([float(t) for t in coordinates])

    def __repr__(self):
        return str(self.coordinates)

    def __add__(self, other):
        coordinates = [a + b for a, b in
                       zip(self.coordinates, other.coordinates)]
        return Vector(coordinates)

    def __mul__(self, multiplier):
        return Vector([t * multiplier for t in self.coordinates])

    def __rmul__(self, multiplier):
        return  self * multiplier

    def __div__(self, divisor):
        return Vector([t / divisor for t in self.coordinates])

    def __sub__(self, other):
        return Vector([x - y for x, y in
                       zip(self.coordinates, other.coordinates)])

    def cross(self, other):
        sc, oc = self.coordinates, other.coordinates
        x = sc[1] * oc[2] - sc[2] * oc[1]
        y = sc[2] * oc[0] - sc[0] * oc[2]
        z = sc[0] * oc[1] - sc[1] * oc[0]
        return Vector(x, y, z)

    def scale(self, scalar):
        return self * scalar

    def normalized(self):
        return self / self.length()

    def dot(self, other):
        return sum([a * b for a, b in
                    zip(self.coordinates, other.coordinates)])

    def fixOrientation(self, xyz):
        return Vector([a * b for a, b in
                       zip(self.coordinates, xyz)])

    def length(self):
        return math.sqrt(self.dot(self))

    def reflectedAt(self, other):
        return self - 2 * other.dot(self) * other
