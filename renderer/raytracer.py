# -*- encoding: utf-8 -*-

from PIL import Image


def _normalizeColor(color, colorDepth):
    '''
    Rechnet RGB-Farben von Float <= 1.0 in die entsprechenden
    Farbwerte der übergebenen Bittiefe um
    @param color: Color-Objekt das umgerechnet werden soll
    @param colorDepth: Farbtiefe des Bildes
    '''
    colorMultiplier = 2 ** colorDepth - 1
    return tuple([int(t * colorMultiplier) for t in color.values])


class RayTracer(object):
    '''
    Objekt zur Kapselung des eigentlichen Rendervorgangs
    '''

    def __init__(self, scene, camera):
        '''
        @param scene: Zu berechnende Szence
        @param camera: Kamera-Objekt
        '''
        self.scene = scene
        self.camera = camera

    def render(self, width, height, colorDepth):
        '''
        Erzeugt aus der übergebenen Szene und Kamera ein RGB-Bild
        @param width: Breite des Bildes
        @param height: Höhe des Bildes
        @param colorDepth: Farbtiefe pro Farbkanal
        '''
        self.camera.setImageSize(width, height)
        self.camera.scene = self.scene
        image = Image.new("RGB", (width, height))
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                color = self.camera.colorAt(x, y)
                pixels[x, y] = _normalizeColor(color, colorDepth)
        return image



