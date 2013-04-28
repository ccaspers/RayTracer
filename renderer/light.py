# -*- encoding: utf-8 -*-


class LightSource(object):
    '''
    Basisklasse für Lichter um Typ einfacher bestimmen zu können
    '''
    pass


class PointLight(LightSource):
    '''
    Punktlicht, das sich in alle Richtungen ausbreitet
    '''

    def __init__(self, position, color):
        '''
        @param position: Position im Raum
        @param color: Farbe der Lichtquelle
        '''
        LightSource.__init__(self)
        self.position = position
        self.color = color
