import pygame
import sys
import math
import utils
import drawer
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
    sim_bodies = []

    body1 = phy.Body(windowSize/2)
    body1.shape.color = bodies_colors[rnd.randint(0, len(bodies_colors)-1)]
    body1.shape.radius = 50
    
    body1.exerceForce = True
    body1.anchored = False
    body1.mass = 10
    body1.penetrationAcceptance = 2
    
    sim_bodies.append(body1)


    body2 = phy.Body(windowSize/2-Vector2(body1.shape.radius))
    body2.shape.color = bodies_colors[rnd.randint(0, len(bodies_colors)-1)]
    body2.shape.radius = 10
    
    body2.exerceForce = True
    body2.anchored = True
    body2.mass = 10
    body2.penetrationAcceptance = 2

    sim_bodies.append(body2)

    # for i in range(10):
    #     body = phy.Body()
    #     body.radius = 10
    #     body.penetrationAcceptance = 1
    #     body.mass = rnd.randint(10, 100)
    #     body.color = bodies_colors[rnd.randint(0, len(bodies_colors)-1)]

    #     sim_bodies.append(body)


    sim = phy.Simulation(window, sim_bodies)
    sim.gravityDir = Vector2(0, 1)
    sim.GC = 5

    
    while True:
        mouseInput = pygame.mouse.get_pressed()
        mousePos = Vector2(pygame.mouse.get_pos())
        # gravityDir = -((mousePos*2 - windowSize) / windowSize).unit
        now = time()
        dt = now - lastTick


        # processed = processInput(wroteText)
        # if processed == False:
        #     break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return exit()

            if event.type == pygame.KEYDOWN:
                if event.key == 27: # Exits on echap
                    return exit()

                if event.key == 1073741904:
                    body2.position += Vector2(-10)
                
                if event.key == 1073741906:
                    body2.position += Vector2(0, -10)

                if event.key == 1073741903:
                    body2.position += Vector2(10)

                if event.key == 1073741905:
                    body2.position += Vector2(0, 10)
                # print(event.key)
        

        # Clear previous render
        window.fill(background_color)

        # Physics
        # F = ma
        # a = F/m
        
        sim.newStep()
        
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
        clock.tick(60)


if __name__=="__main__":

    main()
