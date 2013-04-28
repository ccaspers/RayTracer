# -*- encoding: utf-8 -*-


class Ray(object):
    '''
    Implementiert eine Gerade im Raum
    '''
    def __init__(self, origin, direction):
        '''
        @param origin: Ursprungspunkt der Gerade
        @param direction: Richtungsvektor der Gerade
        '''
        self.origin = origin  # point
        self.direction = direction.normalized()  # vector

    def __repr__(self):
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def __str__(self):
        return self.__repr__()

    def pointAtParameter(self, t):
        '''
        Berechnet den Punkt der Geraden
        @param t: Distanz vom Ursprung der Geraden
        '''
        return self.origin + self.direction.scale(t)
