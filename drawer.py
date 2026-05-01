from pyvectors import *
import pygame
from math import cos, sin

class Shape():
    verticies: [Vector2]
    antialiased = True
    type: str
    # centroid: Vector2

    color = pygame.Color('white')
    
    def __init__(self, verticies: [Vector2], color=None):
        self.verticies = verticies
        self.type = "polygon"
        
        if color is not None:
            self.color = color

    
    def rotate(self, radians):
        for i in range(len(self.verticies)):
            vertex = self.verticies[i]
            direction = -vertex
            xRotation = direction.x * cos(radians) - direction.y * sin(radians)
            yRotation = direction.x * sin(radians) - direction.y * cos(radians)

            self.verticies[i] = Vector2(xRotation, yRotation)
        
       

    def draw(self, surface: pygame.Surface, at: Vector2):
        for i, v1 in enumerate(self.verticies):
            v1 += at
            v2 = self.verticies[i+1-len(self.verticies)] + at
            
            if self.antialiased:
                pygame.draw.aaline(surface, self.color, v1.components, v2.components)
            else:
                pygame.draw.line(surface, self.color, v1.components, v2.components)



class Circle(Shape):
    radius: float

    def __init__(self, radius, color=None):
        self.radius = radius
        self.type = "circle"

        if color is not None:
            self.color = color

    def rotate(self, radians):
        print("Cannot rotate circle (add it later)")

    def draw(self, surface: pygame.Surface, at: Vector2):
        pygame.draw.circle(surface, self.color, at.components, self.radius)


class Rect(Shape):
    width: float
    height: float

    def __init__(self, width: float, height: float, color=None):
        self.width = width
        self.height = height
        self.type = "rect"

        self.verticies = [
            Vector2(-width/2, height/2),
            Vector2(width/2, height/2),
            Vector2(width/2, -height/2),
            Vector2(-width/2, -height/2)
        ]

        if color is not None:
            self.color = color

    def getRect(self, at=Vector2()) -> pygame.Rect:
        return pygame.Rect(at.components, Vector2(self.width, self.height).components)
