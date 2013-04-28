# -*- encoding: utf-8 -*-


class Color(object):
    '''
    Kapselt die Farbkodierung und stellt Methoden zum vereinfachten
    Umgang mit Farben bereit
    '''

    def __init__(self, r, g=0.0, b=0.0):
        '''
        Nimmt 3er Tupel oder drei getrennte Werte als Parameter
        zur Farbdarstellung. Parameter sollten <= 1.0 sein
        @param r: Rotanteil der Farbe
        @param g: Grünanteil der Farbe
        @param b: Blauanteil der Farbe
        '''
        if isinstance(r, (list, tuple)):
            self.values = tuple(r[:3])
        else:
            self.values = (r, g, b)

    def __mul__(self, skalar):
        if type(skalar) is Color:
            return Color([a * b  for a, b
                          in zip(self.values, skalar.values)])
        return Color([t * skalar for t in self.values])

    def __rmul__(self, skalar):
        return  self.__mul__(skalar)

    def __div__(self, skalar):
        return self * (1.0 / float(skalar))

    def __add__(self, other):
        return Color([t + u for t, u in zip(self.values, other.values)])

    def normalized(self):
        '''
        Normalisiert die Farbwerte, falls Überläufe aufgetreten sind
        0.0 <= values <= 1.0
        '''
        values = [self._colorfix(t) for t in self.values]
        return Color(values)

    def _colorfix(self, value):
        value = 1.0 if value > 1.0 else value
        value = 0 if value < 0 else value
        return value
