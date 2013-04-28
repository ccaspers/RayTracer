# -*- encoding: utf-8 -*-

from renderer import Camera
from renderer import PointLight
from renderer import RayTracer
from renderer import Scene

from renderer.geometry import Plane
from renderer.geometry import Sphere
from renderer.geometry import Vector

from renderer.material import Color
from renderer.material import PhongMaterial
from renderer.material import CheckerboardMaterial

# render-settings
RECURSION_DEPTH = 2 # for reflections; should be >= 0
IMAGE_WIDTH = 800   # in pixels
IMAGE_HEIGHT = 600  # in pixels
COLOR_DEPTH = 8     # bit per color-channel

# color-constants
RED   = Color(1.0, 0, 0)
GREEN = Color(0, 1.0, 0)
BLUE  = Color(0, 0, 1.0)
BLACK = Color(0, 0, 0)
WHITE = Color(1, 1, 1)

# material-constants
MAT_RED   = PhongMaterial(RED, reflection=0.2)
MAT_GREEN = PhongMaterial(GREEN, reflection=0.2)
MAT_BLUE  = PhongMaterial(BLUE, reflection=0.2)

def createScene():
    scene = Scene(BLACK)
    scene += Sphere(Vector(2.5, 3, -10), 2, MAT_RED)
    scene += Sphere(Vector(-2.5, 3, -10), 2, MAT_GREEN)
    scene += Sphere(Vector(0, 7, -10), 2, MAT_BLUE)
    scene += Plane(Vector(0, 0, 0), Vector(0, 1, 0), CheckerboardMaterial())
    return scene

def createCamera():
    position = Vector(0, 2, 10)
    up       = Vector(0, 1, 0)
    center   = Vector(0, 3, 0)
    return Camera(45, position, up, center)

def createDefaultLight():
    return [PointLight(Vector(30, 30, 10), WHITE)]

def createFunkyLights():
    lights = []
    lights.append(PointLight(Vector(-30, 30, 10), RED))
    lights.append(PointLight(Vector(0, 30, 10), GREEN))
    lights.append(PointLight(Vector(30, 30, 10), BLUE))
    return lights

if __name__ == "__main__":
    print "running renderer"
    scene = createScene()
#    lights = createDefaultLight()
    lights = createFunkyLights()
    for light in lights:
        scene += light
    camera = createCamera()
    r = RayTracer(scene, camera)
    camera.maxLevel = RECURSION_DEPTH
    r.render(IMAGE_WIDTH, IMAGE_HEIGHT, COLOR_DEPTH).show()
