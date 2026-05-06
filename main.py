import pygame
import sys
import math
import utils
import drawer
import random as rnd
import physics as phy
from pyvectors import *
from time import *

import minigame as game


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


gameSpecialActions = {
    "exit": exit
}

def processInput(data: dict, keyBinds: dict):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return exit()

        if event.type == pygame.KEYDOWN:
            boundInput = keyBinds.get(event.key)
            if boundInput is None: continue
            
            if boundInput["type"] == "action":
                inputData = []
                for dataName in boundInput["requiredData"]:
                    requiredData = data.get(dataName)
                    if not requiredData:
                        raise Exception(f"missing required data ({requiredData}) for input, key: {event.key}")

                    inputData.append(requiredData)

                boundInput["callback"](*inputData)

            elif boundInput["type"] == "specialAction":
                action = gameSpecialActions.get(boundInput["action"])
                if not action:
                    raise Exception(
                        f"missing special action '{boundInput["action"]}', bound to key {event.key}"
                        )

                action()



def main():
    WIDTH = game.windowSize.x
    HEIGHT = game.windowSize.y
    windowSize = game.windowSize
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics")

    background_color = BLACK
    vector_color = GREEN
    bodies_colors = [c for c in colors if c != background_color and c != vector_color]
    sim = game.phySimulation

    inputData = {
        "mousePosition": Vector2()
        }

    lastTick = time()
    
    game.start()
    
    while True:
        mouseInput = pygame.mouse.get_pressed()
        mousePos = Vector2(pygame.mouse.get_pos())
        # gravityDir = -((mousePos*2 - windowSize) / windowSize).unit
        now = time()
        dt = now - lastTick

        inputData["mousePosition"] = mousePos

        processed = processInput(inputData, game.keyBinds)
        if processed == False:
            break
        

        # Clear previous render
        window.fill(background_color)

        # Physics
        # F = ma
        # a = F/m

        game.prePhysics(dt)
        
        sim.newStep()

        # rotation += 0.01
        # body3.rotate(rotation)
        
        for body in sim.bodies:
            body.forces.clear()

            # if mouseInput[0] or mouseInput[2]:
            #     forceType = mouseInput[0] and -1 or 1
            #     distance = body.position - mousePos

            #     if 0 < distance.magnitude < 1e4:
            #         body.forces.append(forceType * distance.unit * 3e4/distance.magnitude)
            
            sim.simulate(body, dt)
            
            body.draw(window)
            utils.drawVectors(window, body.position, body.forces, vector_color)


        # Rendering
        pygame.display.flip() # Update window

        lastTick = now
        clock.tick(60)


if __name__=="__main__":
    main()
