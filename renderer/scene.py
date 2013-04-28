# -*- encoding: utf-8 -*-

from light import LightSource


class Scene(object):
    '''
    Objekt zur Verwaltung von Lichtern, 3D-Objekten und Umgebung
    '''

    def __init__(self, bgcolor):
        '''
        @param bgcolor: Hintergrundfarbe der Szene
        '''
        self.elements = []
        self.lights = []
        self.bgcolor = bgcolor

    def __add__(self, element):
        if isinstance(element, LightSource):
            self.addLight(element)
        else:
            self.addElement(element)
        return self

    def addElement(self, element):
        '''
        Fügt ein 3D-Objekt hinzu
        @param element: 3D-Objekt das hinzugefügt werden soll
        '''
        self.elements.append(element)

    def addLight(self, light):
        '''
        Fügt der Szene eine Lichtquelle hinzu
        @param light: Lichtquelle die hinzugefügt werden soll
        '''
        self.lights.append(light)
