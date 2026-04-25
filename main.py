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
    body1.anchored = True
    body1.mass = 200


    body2 = phy.Body(windowSize/2, vel=Vector2(10, 10))
    body2.color = bodies_colors[rnd.randint(0, len(bodies_colors)-1)]
    body2.exerceForce = True
    body2.anchored = False
    body2.mass = 1

    sim = phy.Simulation(window, [body1, body2])

    
    while True:
        mouseInput = pygame.mouse.get_pressed()
        mousePos = Vector2(pygame.mouse.get_pos())
        # gravityDir = -((mousePos*2 - windowSize) / windowSize).unit
        now = time()
        dt = lastTick - now


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
        
        sim.newStep()
        
        for body in sim.bodies:
            # if mouseInput[0] or mouseInput[2]:
            #     forceType = mouseInput[0] and 1 or -1
            #     distance = body.position - mousePos
                
            #     if distance.magnitude < 1e4:
            #         body.forces.append(forceType * distance.unit * 3e4/distance.magnitude)
            #         # forceSum += -(body.position - mousePos).unit * 10
            
            sim.simulate(body, dt)

            body.draw(window)

        # for body in bodies:
        #     if not body.anchored:
        #         relPos = body.getRelativePos(windowSize)
                
        #         # forces = []
        #         # forceSum = Vector2()
                

        #         if gravityDir.magnitude > 0:
        #             g = body.mass * G
        #             gF: Vector2 = g * gravityDir

        #             body.forces.append(gF)
        #             # forceSum += gF


                

        #         phy_bodies.remove(body)
        #         for other in phy_bodies:
        #             # Continues if no interactions between bodies
        #             if not body.exerceForce and not other.exerceForce: continue
        #             distance = body.position - other.position
                    

        #             if distance.magnitude-body.radius-other.radius < 0 and body.canCollide and other.canCollide:
        #                 print('collision')


        #             if distance.magnitude != 0:
        #                 direction = distance.unit
        #                 bodyGF = GC*(body.mass*other.mass / distance.magnitude**2)
                        

        #                 # other exerce a force on body
        #                 if other.exerceForce:
        #                     body.forces.append(bodyGF*direction)

        #                 # body exerce a force on other if other is not anchored
        #                 if body.exerceForce and not other.anchored:
        #                     other.forces.append(-bodyGF*direction) 


                    

        #         # print(phy_bodies)
                

                

        #         # Collision Y
        #         if abs(relPos.y) + body.radius > HEIGHT:
        #             normal = Vector2(0, utils.sign(relPos.y))

        #             # print("COllide Y")
        #             if body.velocity > Vector2.zero:
        #                 diff = normal.dot(body.velocity.unit) * .4

        #                 # forceSum += gF * normal.dot(gF.unit)
        #                 for i in range(len(body.forces)):
        #                     force = body.forces[i]
        #                     if force.magnitude > 0:
        #                         body.forces.append(force * normal.dot(force.unit)* 1.1)
                        

        #                 body.velocity = Vector2(body.velocity.x, body.velocity.y * -diff)

                

        #         # Collision X
        #         if abs(relPos.x) + body.radius > WIDTH:
        #             normal = Vector2(utils.sign(relPos.x))
        #             # print("Collide X")

                    

        #             if body.velocity > Vector2.zero:
        #                 diff = normal.dot(body.velocity.unit) * .4

                        
        #                 # forceSum += gF * normal.dot(gF.unit)

        #                 for i in range(len(body.forces)):
        #                     force = body.forces[i]
        #                     if force.magnitude > 0:
        #                         body.forces.append(force * normal.dot(force.unit) * 1.1)

                        
        #                 body.velocity = Vector2(body.velocity.x * -diff, body.velocity.y)
                        


                

        #         if len(body.forces) != 0:
        #             acc = vsum(body.forces)/body.mass * dt
        #             body.accelerate(acc)
        #             body.updatePos()

            

            # body.draw(window)
            # drawVectors(window, body.position, body.forces, color=GREEN)

            # body.forces.clear()

        

        

        # Rendering
        pygame.display.flip() # Update window

        lastTick = now
        clock.tick(60)


if __name__=="__main__":

    main()
