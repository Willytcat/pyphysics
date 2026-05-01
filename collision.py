import math
import utils
from pyvectors import *
import pygame

class Collider():
    verticies: [Vector2]
    normals: [Vector2]

    active = True

    def __init__(self, verticies):
        self.verticies = verticies
        self.calcNormals()


    def calcNormals(self):
        self.normals.clear()

        for i, v1 in enumerate(self.verticies):
            v2 = self.verticies[i+1-len(self.verticies)]

            edge = v2 - v1
            self.normals[i] = edge.normal


class BoxCollider(Collider):
    width: float
    height: float
    
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.verticies = [
            Vector2(-width/2, height/2),
            Vector2(width/2, height/2),
            Vector2(width/2, -height/2),
            Vector2(-width/2, -height/2),
        ]
        self.calcNormals()

class CircleCollider(Collider):
    radius: float

    def __init__(self, radius):
        self.radius = radius


class CollisionManifold():
    point: Vector2
    normal: Vector2
    depth: float

    def __init__(self, point, depth, normal):
        self.point = point
        self.depth = depth
        self.normal = normal

    def draw(self, window):
        depthVector = self.normal*self.depth
        utils.drawVector(window, self.point-depthVector, depthVector, (0,255,0))
        pygame.draw.circle(window, (255,0,0), self.point, 4)



def circlesIntersection(p1, c1: CircleCollider, p2, c2: CircleCollider):
    distance = p2 - p1
    penetrationDepth = c1.radius+c2.radius - distance.magnitude
    
    if penetrationDepth > 0:
        normal = Vector2(1)
        penetrationPoint = p1 + normal*c1.radius
        
        if distance.magnitude != 0:
            normal = distance.unit

        return CollisionManifold(penetrationPoint, penetrationDepth, normal)
