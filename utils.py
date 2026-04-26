from pyvectors import *
import pygame

def isSequence(v):
    return type(v) is list or type(v) is tuple

def validIndex(l, i):
    return -len(l) <= i < len(l)

def sign(n):
    if n < 0:
        return -1
    else:
        return 1


def drawVector(surface, at: Vector2, vector: Vector2, color, arrowLength=3, arrowWidth=1):
    if vector.magnitude == 0:
        return

    end = at + vector
    arrowHeadCenter = at + vector * (1 - arrowLength / vector.magnitude)

    pygame.draw.aalines(surface, color, False,
        (
        at.components,
        end.components,

        (arrowHeadCenter + vector.normal * arrowWidth).components,
        (arrowHeadCenter - vector.normal * arrowWidth).components,
        end.components
        )
    )

def drawVectors(surface, at: Vector2, vectorList: list, color, arrowLength=3, arrowWidth=1):
    for v in vectorList:
        drawVector(surface, at, v, color, arrowLength, arrowWidth)
