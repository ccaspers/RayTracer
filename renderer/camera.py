# -*- encoding: utf-8 -*-

import math
from ray import Ray
from material.color import Color


class Camera(object):
    '''
    Kameraobjekt kapselt Berechnung der Farbtöne einzelner
    Pixel einer 3D-Szene
    '''
    DEFAULT_WIDTH = 320
    DEFAULT_HEIGHT = 240
    MAX_DISTANCE = float('inf')
    EPSILON = 0.0001

    def __init__(self, fov, position, upVector, focusPoint):
        '''
        @param fov: Field of View der Kamera
        @param position: Position der Kamera im Raum
        @param upVector: Vektor der Drehung der Kamera definiert
        @param focusPoint: Punkt auf den Kamera schaut
        '''
        self.alpha = 0
        self.height = 0
        self.width = 0
        self.pixelWidth = 0
        self.pixelHeight = 0
        self.scene = None
        self.maxLevel = 0
        self.fov = fov
        self.position = position
        self.f = (focusPoint - position).normalized()
        self.s = self.f.cross(upVector).normalized()
        self.u = self.s.cross(self.f).fixOrientation((1, -1, 0))
        self.setImageSize(Camera.DEFAULT_WIDTH, Camera.DEFAULT_HEIGHT)

    def calcRay(self, x, y):
        '''
        Berechnet für jede Koordinate genau einen Strahl
        @param x: x-Koordinate des zu berechnenden Pixels
        @param y: y-Koordinate des zu berechnenden Pixels
        '''
        xcomp = self.s * (x * self.pixelWidth - self.width / 2)
        ycomp = self.u * (y * self.pixelHeight - self.height / 2)
        ray = Ray(self.position, self.f + xcomp + ycomp)
        return ray

    def setImageSize(self, width, height):
        '''
        Konfiguriert die Kamera für die übergebene Bildgröße
        @param width: Breite des Bildes
        @param height: Höhe des Bildes
        '''
        self.alpha = math.radians(self.fov / 2)
        self.height = 2 * math.tan(self.alpha)
        self.width = self.height * (float(width) / float(height))
        self.pixelWidth = self.width / (width - 1)
        self.pixelHeight = self.height / (height - 1)

    def colorAt(self, x, y):
        '''
        Berechnet die Farbe eines Pixels, startet die Rekursion
        @param x: x-Koordinate
        @param y: y-Koordinate
        '''
        recursionLevel = 0
        ray = self.calcRay(x, y)
        color = self.traceRay(recursionLevel, ray)
        return color.normalized()

    def isDirectLight(self, hitPoint, light):
        '''
        Prüft ob vom getroffenen Objektpunkt direkte
        Sicht auf die Lichtquelle vorhanden ist
        @param hitPoint: Punkt auf Objekt
        @param light: zu prüfende Lichtquelle
        '''
        hitRay = Ray(hitPoint, light.position - hitPoint)
        for element in self.scene.elements:
            hitdist = element.intersectionParameter(hitRay)
            if hitdist and hitdist > Camera.EPSILON:
                return False
        return True

    def filterLights(self, hitPoint):
        '''
        Sucht alle Lichtquellen der Szene, die den getroffenen
        Punkt direkt anstrahlen
        @param hitPoint: zu prüfender Punkt
        '''
        return [light for light in self.scene.lights
                if self.isDirectLight(hitPoint, light)]

    def traceRay(self, currentLevel, ray):
        '''
        Verfolgt einen Strahl bis zum Schnittpunkt mit einem
        Objekt oder der maximalen Sichtweite der Kamera.
        Gibt Farbe am Schnittpunkt oder Hintergrundfarbe zurück
        @param currentLevel: aktuelle Rekursionstiefe
        @param ray: zu verfolgender Strahl
        '''
        if currentLevel <= self.maxLevel:
            element, point = self.intersect(ray)
            if element and point:
                return self.shade(currentLevel, element, point, ray)
        return self.scene.bgcolor

    def shade(self, currentLevel, element, point, ray):
        '''
        Berechnet den Farbton eines getroffenen Elements am Schnittpunkt
        @param currentLevel: aktuelle Rekursionstiefe
        @param element: getroffenes Element
        @param point: Schnittpunkt
        @param ray: Strahl der Element getroffen hat
        '''
        materialReflection = element.material.reflection
        reflectedColor = Color(0, 0, 0)
        directColor = self.computeDirectLight(element, point, ray)
        if materialReflection > 0:
            reflectedRay = self.computeReflectedRay(element, point, ray)
            reflectedColor = self.traceRay(currentLevel + 1, reflectedRay)
        return directColor + materialReflection * reflectedColor

    def computeDirectLight(self, element, point, ray):
        '''
        Errechnet nur den Elementeigenen Farbton (siehe Material)
        @param element: Element
        @param point: Punkt dessen Farbe berechnet werden soll
        @param ray: Strahl der Element getroffen hat
        '''
        directLights = self.filterLights(point)
        color = element.colorAt(point, directLights, ray)
        return color

    def computeReflectedRay(self, element, point, ray):
        '''
        Reflektiert den übergbenen Strahl an der Normalen
        des getroffenen Elements der Szene
        @param element: getroffenes Element
        @param point: Schnittpunkt
        @param ray: zu reflektierender Strahl
        '''
        normal = element.normalAt(point)
        direction = ray.direction.reflectedAt(normal)
        return Ray(point, direction)

    def intersect(self, ray):
        '''
        Sucht das Element der Szene, das in minimaler Distanz vom übergebenen
        Strahl geschnitten wird. Liefert Element und Schnittpunkt zurück
        @param ray: Strahl der auf Schnittpunkte geprüft werden soll
        '''
        hitElement, hitPoint = None, None
        maxDistance = Camera.MAX_DISTANCE
        for element in self.scene.elements:
            hitDistance = element.intersectionParameter(ray)
            if hitDistance and hitDistance < maxDistance and hitDistance > 0:
                maxDistance = hitDistance
                hitPoint = ray.pointAtParameter(hitDistance)
                hitElement = element
        return hitElement, hitPoint
