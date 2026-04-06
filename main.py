import pygame
import sys
import math

import utils
from pyvectors import *
from time import *


# Initialisations
pygame.init()
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Body():
    position: Vector2
    velocity: Vector2
    # acceleration: Vector2
    mass: int = 1

    radius: float = 1
    color: tuple = BLACK

    def __init__(self, pos, vel=Vector2(), mass=1, color=BLACK, radius=10):
        self.position = pos
        self.velocity = vel
        # self.acceleration = Vector2()
        self.mass = mass
        
        self.color = color
        self.radius = radius
        

    def accelerate(self, acc):
        self.velocity += acc

    def updatePos(self):
        self.position += self.velocity

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.position.components, self.radius)

    def getRelativePos(self, surfaceSize: Vector2):
        return self.position*2 - surfaceSize



def exit():
    print("Exits with success!")
    pygame.quit()
    sys.exit()
            
    return 0


def processInput(wrote: str):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return exit()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == 27: # Exits on echap
                return exit()
            elif event.key == 127: # Reset on suppr
                return 1
            elif event.key == 8: # Delete wrote text
                wrote = wrote[:-1]
            elif event.key == 1073741892: # Toggles full screen
                pygame.display.toggle_fullscreen()
            
        if event.type == pygame.TEXTINPUT:
            wrote += event.text
    
    return wrote


def main():
    WIDTH = 800
    HEIGHT = 600
    windowSize = Vector2(WIDTH, HEIGHT)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics")

    gravityDir = -Vector2.yAxis
    wroteText = ""
    G = 9.81

    lastTick = time()

    bodies = [
        Body(windowSize/2),
        Body(windowSize/3, vel=Vector2(10))
    ]

    while True:
        processed = processInput(wroteText)
        if processed == 0:
            break
        elif processed == 1:
            wroteText = ""
            pos = Vector2(window.get_width()/2, window.get_height()/2)
        elif type(processed) is str:
            wroteText = processed


        mouseInput = pygame.mouse.get_pressed()
        mousePos = Vector2(pygame.mouse.get_pos())
        # gravityDir = -((mousePos*2 - windowSize) / windowSize).unit
        
        now = time()
        dt = lastTick - now

        # Clear previous render
        window.fill(WHITE)
        window.set_alpha(0.5)
        
        # Object
        # font = pygame.font.SysFont("arial", 36)
        # text_render = font.render(wroteText, True, BLACK)
        
        
        # physics
        # F = ma
        # a = F/m

        for body in bodies:
            relPos = body.getRelativePos(windowSize)
            forces = []
            # forceSum = Vector2()

            g = body.mass * G
            gF: Vector2 = g * gravityDir
            forces.append(gF)
            # forceSum += gF

            if mouseInput[0]:
                print("repulsive force")
                forces.append(-(body.position - mousePos).unit * 10)
                # forceSum += -(body.position - mousePos).unit * 10

            # Collision Y
            if abs(relPos.y) + body.radius > HEIGHT:
                normal = Vector2(0, utils.sign(relPos.y))
                
                diff = normal.dot(body.velocity.unit) * .4
                # forceSum += gF * normal.dot(gF.unit)
                for force in forces:
                    if force.magnitude > 0:
                        forces.append(force * normal.dot(force.unit))

                body.velocity = Vector2(body.velocity.x, body.velocity.y * -diff)
            
            # Collision X
            if abs(relPos.x) + body.radius > WIDTH:
                normal = Vector2(utils.sign(relPos.x))

                diff = normal.dot(body.velocity.unit) * .4

                # forceSum += gF * normal.dot(gF.unit)
                for force in forces:
                    if force.magnitude > 0:
                        forces.append(force * normal.dot(force.unit))

                body.velocity = Vector2(body.velocity.x * -diff, body.velocity.y)

            
            acc = vsum(forces)/body.mass * dt
            body.accelerate(acc)
            body.updatePos()

            
            body.draw(window)
            drawVector(window, body.position, -gF * 2, color=GREEN)
        
        # Rendering
        pygame.display.flip() # Update window
        
        lastTick = now
        clock.tick(60)




def drawVector(surface: pygame.Surface, at: Vector2, vector: Vector2, color=BLACK, arrowLength=3, arrowWidth=1):
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


if __name__=="__main__":
    main()