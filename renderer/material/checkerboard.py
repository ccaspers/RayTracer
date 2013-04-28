# -*- encoding: utf-8 -*-

from color import Color
from phong import PhongMaterial


class CheckerboardMaterial(PhongMaterial):

    def __init__(self, baseColor=Color(1, 1, 1),
                 otherColor=Color(0.1, 0.1, 0.1),
                 ambient=0.1, diffuse=0.8, specular=0.2,
                 reflection=0.2, smoothness=0.5, checkSize=2.0):
        '''
        @param baseColor: erste Farbe des Schachbretts
        @param otherColor: zweite Farbe des Schachbretts
        @param ambient: konstanter ambienter Anteil <= 1
        @param diffuse: diffuser Anteil <= 1
        @param specular: spekularer Anteil <= 1
                         specular + diffuse <= 1
        @param reflection: reflection <= 1, hat einfluss auf Spiegelungen
                           anderer Objekte
        @param smoothness: 0 = rauh, > 32 perfekter Spiegel
        @param checkSize: Kachelgröße
        '''
        PhongMaterial.__init__(self, baseColor, ambient, diffuse,
                               specular, reflection, smoothness)
        self.otherColor = otherColor
        self.checkSize = checkSize

    def baseColorAt(self, point):
        '''
        Sucht die Grundfarbe des Materials am übergebenen Punkt
        @param point: Punkt an dessen Stelle Grundfarbe gesucht werden soll
        '''
        coordinates = point.scale(1.0 / self.checkSize).coordinates
        if sum([int(abs(t) + 0.5) for t in coordinates]) % 2:
            return self.otherColor
        return self.color
