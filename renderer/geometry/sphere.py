# -*- encoding: utf-8 -*-

import math


class Sphere(object):
    def __init__(self, focusPoint, radius, material):
        self.material = material
        self.center = focusPoint  # point
        self.radius = radius  # scalar

    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = (self.radius * self.radius) - (co.dot(co) - v * v)
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalized()

    def colorAt(self, point, lights, ray):
        normal = self.normalAt(point)
        return self.material.renderColor(normal, point, lights, ray)
