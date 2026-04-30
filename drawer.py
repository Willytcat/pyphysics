from pyvectors import *
import pygame

class Shape():
    verticies: [Vector2]
    antialiased = True

    color = pygame.Color('white')
    
    def __init__(self, verticies: [Vector2], color=None):
        self.verticies = verticies
        
        if color is not None:
            self.color = color

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

        if color is not None:
            self.color = color

    def draw(self, surface: pygame.Surface, at: Vector2):
        pygame.draw.circle(surface, self.color, at.components, self.radius)


class Rect(Shape):
    width: float
    height: float

    def __init__(self, width: float, height: float, color=None):
        self.width = width
        self.height = height

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
