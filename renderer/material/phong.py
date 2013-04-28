# -*- encoding: utf-8 -*-

from color import Color


class PhongMaterial(object):
    '''
    Material, dass das Phong-Beleuchtungsmodell umsetzt
    '''

    def __init__(self, color=Color(0.5, 0.5, 0.5),
                 ambient=0.3, diffuse=0.7, specular=0.3,
                 reflection=0.0, smoothness=10.0):
        '''
        @param color: Grundfarbe des Materials
        @param ambient: konstanter ambienter Anteil <= 1
        @param diffuse: diffuser Anteil <= 1
        @param specular: spekularer Anteil <= 1
                         specular + diffuse <= 1
        @param reflection: reflection <= 1, hat einfluss auf Spiegelungen
                           anderer Objekte
        @param smoothness: 0 = rau, > 32 glatt
        '''
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.smoothness = smoothness

    def renderColor(self, normal, hitpoint, lights, ray):
        '''
        Berechnet den Farbton des Materials an der Stelle des Objekts
        @param normal: Normalenvektor an der Stelle die vom Kamera-Strahl
                       geschnitten wurden
        @param hitpoint: Schnittpunkt von Kamera-Strahl und Objekt
        @param lights: Alle Lichtquellen der Szene
        @param ray: Strahl der von der Kamera in die Szene 'geschossen' wurde
                    bzw. reflektierter Lichtstrahl bei rekursivem tracing
        '''
        color = self._ambientColor(hitpoint)
        for light in lights:
            vLight = (light.position - hitpoint).normalized()
            color += self._diffuseColor(normal, hitpoint, light, vLight)
            color += self._specularColor(normal, light, vLight, ray)
        return color

    def baseColorAt(self, point):
        '''
        Sucht die Grundfarbe des Materials am übergebenen Punkt
        Wird hier nicht berücksichtigt. Ist allerdings Konvention für alle
        Materialien
        @param point: Punkt an dessen Stelle Grundfarbe gesucht werden soll
        '''
        return self.color

    def _ambientColor(self, point):
        '''
        Berechnet den ambienten Farbanteil des Materials
        '''
        return self.baseColorAt(point) * self.ambient

    def _diffuseColor(self, normalAtPoint, point, light, vLight):
        '''
        Berechnet den diffusen Farbanteil des Materials und berücksichtig
        Absorption durch die Materialfarbe
        @param normalAtPoint: Normalenvektor am Punkt des Objekts
        @param light: Lichtquelle für die der diffuse Anteil berechnet wird
        @param vLight: Vektor von Punkt auf Objekt zu Lichtquelle
        '''
        lightDotNormal = vLight.dot(normalAtPoint)
        lightDotNormal = 0 if lightDotNormal < 0 else lightDotNormal
        color = self.baseColorAt(point)
        return light.color * color * self.diffuse * lightDotNormal

    def _specularColor(self, normalAtPoint, light, vLight, ray):
        '''
        Berechnet den spekularen Anteil des Materials
        @param normalAtPoint: Normalenvektor am Punkt des Objekts
        @param light: Lichtquelle für die spekuklares Licht berechnet wird
        @param vLight: Vektor vom Punkt des Objekts zur Lichtquelle
        @param ray: Strahl der von Kamera auf Objekt 'geschossen' wurde
        '''
        lightReflected = vLight.reflectedAt(normalAtPoint).normalized() * -1
        dotproduct = lightReflected.dot((-1 * ray.direction).normalized())
        dotproduct = dotproduct if dotproduct > 0 else 0
        return light.color * self.specular * (dotproduct ** self.smoothness)
