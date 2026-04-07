import pygame
import sys
import math
import random as rnd
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

colors = [BLACK, WHITE, RED, GREEN, BLUE]


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
def reset(bodies: [Body], to: Vector2, vel=Vector2()):
    for body in bodies:
        body.position = to
        body.velocity = vel

def processInput(wrote: str, bodies):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return exit()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == 27: # Exits on echap
                return exit()
            elif event.key == 127: # Reset on suppr
                wrote = ""
                return 1
            elif event.key == 8: # Delete wrote text
                wrote = wrote[:-1]
            elif event.key == 1073741892: # Toggles full screen
                pygame.display.toggle_fullscreen()
            
            elif event.key == 97:
                bodies.append(Body(Vector2()))
            
        if event.type == pygame.TEXTINPUT:
            wrote += event.text
    
    return wrote


def main():
    WIDTH = 1920
    HEIGHT = 1080
    windowSize = Vector2(WIDTH, HEIGHT)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics")
    wroteText = ""
    
    # gravityDir = -Vector2.yAxis #Vector2.zero
    gravityDir = Vector2.zero
    G = 9.81
    GC = 6.67430e1 #e-11
    lastTick = time()
    
    background_color = BLACK
    bodies_colors = [c for c in colors if c != background_color]
    bodies = []
    for i in range(rnd.randint(2, 3)):
        bodies.append(Body(
            windowSize/rnd.uniform(2, 3),
            # Vector2(rnd.uniform(-10, 10), rnd.uniform(-10, 10)),
            mass=rnd.randint(1, 20),
            color=bodies_colors[rnd.randint(0, len(bodies_colors) - 1)],
            radius=rnd.randint(10, 20)
        ))
    
    while True:
        processed = processInput(wroteText, bodies)
        if processed == 0:
            break
        elif processed == 1:
            reset(bodies, windowSize/2)
        elif type(processed) is str:
            wroteText = processed

        mouseInput = pygame.mouse.get_pressed()
        mousePos = Vector2(pygame.mouse.get_pos())
        # gravityDir = -((mousePos*2 - windowSize) / windowSize).unit
        
        now = time()
        dt = lastTick - now
        # Clear previous render
        window.fill(background_color)
        
        # Object
        # font = pygame.font.SysFont("arial", 36)
        # text_render = font.render(wroteText, True, BLACK)
        
        
        # physics
        # F = ma
        # a = F/m
        phy_bodies = list(bodies)

        for body in bodies:
            relPos = body.getRelativePos(windowSize)
            
            forces = []
            forceSum = Vector2()
            
            
            g = body.mass * G
            gF: Vector2 = g * gravityDir
            forces.append(gF)
            # forceSum += gF

            # phy_bodies.remove(body)
            for other in phy_bodies:
                distance = body.position - other.position
                
                if distance.magnitude != 0:
                    direction = distance.unit
                    bodyGF = GC*(body.mass*other.mass / distance.magnitude**2)
                    forces.append(bodyGF*direction)



                
            # print(phy_bodies)
            
            
            if mouseInput[0] or mouseInput[2]:
                forceType = mouseInput[0] and 0.5 or -1
                distance = body.position - mousePos
                if distance.magnitude < 1e4:
                    forces.append(forceType * distance.unit * 3e4/distance.magnitude)
                    # forceSum += -(body.position - mousePos).unit * 10
            
            
            # Collision Y
            # if abs(relPos.y) + body.radius > HEIGHT:
            #     normal = Vector2(0, utils.sign(relPos.y))
            #     print("COllide Y")

            #     if body.velocity > Vector2.zero:
            #         diff = normal.dot(body.velocity.unit) * .6
                    
            #         # forceSum += gF * normal.dot(gF.unit)
            #         for i in range(len(forces)):
            #             force = forces[i]
            #             if force.magnitude > 0:
            #                 forces.append(force * normal.dot(force.unit)* 1.3)
                    
            #         body.velocity = Vector2(body.velocity.x, body.velocity.y * -diff)
            
            # # Collision X
            # if abs(relPos.x) + body.radius > WIDTH:
            #     normal = Vector2(utils.sign(relPos.x))
            #     print("Collide X")
                
            #     if body.velocity > Vector2.zero:
            #         diff = normal.dot(body.velocity.unit) * .6
                    
            #         # forceSum += gF * normal.dot(gF.unit)
            #         for i in range(len(forces)):
            #             force = forces[i]
            #             if force.magnitude > 0:
            #                 forces.append(force * normal.dot(force.unit) * 1.3)
                    
            #         body.velocity = Vector2(body.velocity.x * -diff, body.velocity.y)
                    
            
            # acc = vsum(forces)/body.mass * dt
            acc = vsum(forces)/body.mass * dt
            body.accelerate(acc)
            body.updatePos()
            
            body.draw(window)
            drawVectors(window, body.position, forces, color=GREEN)
        
        
        # Rendering
        pygame.display.flip() # Update window

        lastTick = now
        clock.tick(60)
 


def drawVectors(surface: pygame.Surface, at: Vector2, vectorList: list, color=BLACK, arrowLength=3, arrowWidth=1):
    for v in vectorList:
        drawVector(surface, at, v, color, arrowLength, arrowWidth)

def drawVector(surface: pygame.Surface, at: Vector2, vector: Vector2, color=BLACK, arrowLength=3, arrowWidth=1):
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

if __name__=="__main__":
    main()
