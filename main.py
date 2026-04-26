import pygame
import sys
import math
import utils
import random as rnd
import physics as phy
from pyvectors import *
from time import *


Color = pygame.color.Color


pygame.init()
clock = pygame.time.Clock()

BLACK = Color('black')
WHITE = Color('white')
GREEN = Color('green')
RED = Color('red')
BLUE = Color('blue')
YELLOW = Color('yellow')
colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW]
 

def exit():
    print("Exits with success!")
    pygame.quit()
    sys.exit()

    return False



def processInput(wrote: str):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return exit()

        

        if event.type == pygame.KEYDOWN:
            if event.key == 27: # Exits on echap
                return exit()

            # elif event.key == 127: # Reset on suppr
            #     wrote = ""
            #     return 1

            # elif event.key == 8: # Delete wrote text
            #     wrote = wrote[:-1]

            # elif event.key == 1073741892: # Toggles full screen
            #     pygame.display.toggle_fullscreen()

            # elif event.key == 97:
            #     return 'newBody'
            
        if event.type == pygame.TEXTINPUT:
            wrote += event.text

    return wrote




def main():
    WIDTH = 800
    HEIGHT = 800
    windowSize = Vector2(WIDTH, HEIGHT)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics")
    wroteText = ""
    lastTick = time()


    background_color = BLACK
    vector_color = GREEN
    bodies_colors = [c for c in colors if c != background_color and c != vector_color]

    body1 = phy.Body(windowSize/2)
    body1.color = bodies_colors[rnd.randint(0, len(bodies_colors)-1)]
    body1.exerceForce = True
    body1.anchored = False
    body1.mass = 100


    body2 = phy.Body(windowSize/2)
    body2.color = bodies_colors[rnd.randint(0, len(bodies_colors)-1)]
    body2.exerceForce = True
    body2.anchored = False
    body2.mass = 10

    sim = phy.Simulation(window, [body1, body2])
    sim.gravityDir = Vector2(0, 1)

    
    while True:
        mouseInput = pygame.mouse.get_pressed()
        mousePos = Vector2(pygame.mouse.get_pos())
        # gravityDir = -((mousePos*2 - windowSize) / windowSize).unit
        now = time()
        dt = now - lastTick


        processed = processInput(wroteText)
        if processed == False:
            break

        # elif processed == 'newBody':
        #     newBody = phy.Body(mousePos, color=bodies_colors[rnd.randint(0, len(bodies_colors) - 1)])
        #     newBody.mass = 100
        #     newBody.exerceForce = True
        #     bodies.append(newBody)

        # elif type(processed) is str:
        #     wroteText = processed
        

        # Clear previous render
        window.fill(background_color)


        # Object
        # font = pygame.font.SysFont("arial", 36)
        # text_render = font.render(wroteText, True, BLACK)

        

        # physics
        # F = ma
        # a = F/m
        
        # sim.newStep()
        
        for body in sim.bodies:
            body.forces.clear()

            if mouseInput[0] or mouseInput[2]:
                forceType = mouseInput[0] and -1 or 1
                distance = body.position - mousePos

                if 0 < distance.magnitude < 1e4:
                    body.forces.append(forceType * distance.unit * 3e4/distance.magnitude)
            
            sim.simulate(body, dt)
            
            body.draw(window)
            utils.drawVectors(window, body.position, body.forces, vector_color)

        # Rendering
        pygame.display.flip() # Update window

        lastTick = now
        clock.tick(50)


if __name__=="__main__":

    main()
