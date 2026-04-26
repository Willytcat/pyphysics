import math
import pygame
import utils
from time import time
from pyvectors import *

## Conventions:
# dt == delta time


Color = pygame.color.Color

class Body():
    position: Vector2
    velocity: Vector2
    mass: int = 1
    forces: list
    anchored : bool = False
    exerceForce: bool = False
    canCollide: bool = True
    
    radius: float = 10
    color: Color = Color(255, 255, 255)
    
    
    def __init__(self, pos, vel=Vector2(), color=None, radius=None):
        self.position = pos
        self.velocity = vel
        
        if color is not None:
            self.color = color
        if radius is not None:
            self.radius = radius
        
        self.forces = []

    def __str__(self):
        return f"Body at {self.position}"
        
    def accelerate(self, acc):
        self.velocity += acc
    
    def updatePos(self):
        self.position += self.velocity

    def resolveForces(self, dt: float):
        if len(self.forces) == 0: return
        
        acc = vsum(self.forces)/self.mass * dt
        self.accelerate(acc)
        self.forces.clear()
    
    def draw(self, window):
        pygame.draw.circle(window, self.color, self.position.components, self.radius)
    
    def getRelativePos(self, surfaceSize: Vector2):
        return self.position*2 - surfaceSize


class Constraint():
    active = True

    def __init__(self):
        print("new constraint")


    

class Simulation():
    window: pygame.Surface
    lastCall = 0
    
    bodies: [Body]
    _phyBodies: [Body]

    G = 9.81
    GC = 6.67
    gravityDir = Vector2(0, 1)

    def __init__(self, window, bodies):
        self.window = window
        self.bodies = bodies
        self.lastCall = time()
    
    def newStep(self):
        self._phyBodies = list(self.bodies)

        now = time()
        self.lastCall = now

        return now - self.lastCall
    
    def step(self) -> float:
        dt = self.newStep()

        for i, body in enumerate(self.bodies):
            # sim._phyBodies.pop()
            
            self.simulate(body, dt)
        
        return dt

    def simulate(self, body: Body, dt):
        if body.anchored: return

        # body.forces.clear()

        windowSize = Vector2(self.window.get_size())
        relPos = body.getRelativePos(windowSize)

        if self.gravityDir.magnitude > 0:
            g = body.mass * self.G
            body.forces.append(g * self.gravityDir)


        # borderNormal = relPos // windowSize
        # print(borderNormal)
        
        # if borderNormal.magnitude > 1:
        #     if body.velocity > Vector2.zero:
        #         diff = borderNormal.dot(body.velocity.unit) * .4
        #         body.velocity *= -diff
            
        #     for force in body.forces:
        #             if force.magnitude > 0:
        #                 body.forces.append(force * borderNormal.dot(force.unit) * 1.1)
        # print(relPos)
        if abs(relPos.y) + body.radius > 800:
            normal = Vector2(0, -utils.sign(relPos.y))
            penetrationDepth = abs(relPos.y) + body.radius - 800

            if body.velocity > Vector2.zero:
                diff = normal.dot(body.velocity.unit) * .5
                body.velocity = Vector2(body.velocity.x, body.velocity.y * -diff)
            
            for i in range(len(body.forces)):
                force = body.forces[i]
                if force.magnitude > 0:
                    body.forces.append(force * normal.dot(force.unit) * penetrationDepth/1)

            body.position += normal * penetrationDepth/body.mass
            # body.forces.append(penetrationDepth * nonCorrectedCount * 3 * normal)
        
        # Collision X
        if abs(relPos.x) + body.radius > 800:
            normal = Vector2(-utils.sign(relPos.x))
            penetrationDepth = abs(relPos.x) + body.radius - 800

            # if penetrationDepth > 0:
            #     body.position += Vector2(penetrationDepth * -utils.sign(relPos.x))
            body.forces.append(penetrationDepth* 3 * normal)

            if body.velocity > Vector2.zero:
                diff = normal.dot(body.velocity.unit) * .5
                body.velocity = Vector2(body.velocity.x * -diff, body.velocity.y)

            nonCorrectedCount = 0
            for i in range(len(body.forces)):
                force = body.forces[i]
                if force.magnitude > 0:
                    diff = normal.dot(force.unit)
                    # if diff == 0:
                    #     print("Non countered force x")
                    #     nonCorrectedCount += 1
                    # else:
                    body.forces.append(force * normal.dot(force.unit) * penetrationDepth/1)

            body.forces.append(penetrationDepth * 3 * normal)
            
        acc = vsum(body.forces) / body.mass * dt
        body.accelerate(acc)
        body.updatePos()


# def simulate(sim: Simulation, body: Body, dt=None):
#     if dt is None:
#         now = time()
#         dt = now - sim.lastCall
#         sim.lastCall = now

#     if body.anchored: return
#     relPos = body.getRelativePos(Vector2(sim.window.get_size()))
    

#     # for other in sim._phyBodies:
#     #     # Continues if no interactions between bodies
#     #     if not body.exerceForce and not other.exerceForce: continue
        
#     #     distance = body.position - other.position
        
#     #     if distance.magnitude-body.radius-other.radius < 0 and body.canCollide and other.canCollide:
#     #         print('collision')
#     #     if distance.magnitude != 0:
#     #         direction = distance.unit
#     #         bodyGF = GC*(body.mass*other.mass / distance.magnitude**2)
            
#     #         # other exerce a force on body
#     #         if other.exerceForce:
#     #             body.forces.append(bodyGF*direction)
            
#     #         # body exerce a force on other if other is not anchored
#     #         if body.exerceForce and not other.anchored:
#     #             other.forces.append(-bodyGF*direction)
    
    
#     borderNormal = Vector2(sim.window.get_size()) // relPos
#     print(borderNormal)
#     if -1 >= borderNormal.magnitude <= 1:
#         print("bound")
#     # Collision Y
#     # if abs(relPos.y) + body.radius > HEIGHT:
#     #     normal = Vector2(0, utils.sign(relPos.y))
#     #     # print("COllide Y")
#     #     if body.velocity > Vector2.zero:
#     #         diff = normal.dot(body.velocity.unit) * .4
            
#     #         # forceSum += gF * normal.dot(gF.unit)
#     #         for i in range(len(body.forces)):
#     #             force = body.forces[i]
#     #             if force.magnitude > 0:
#     #                 body.forces.append(force * normal.dot(force.unit)* 1.1)
            
#     #         body.velocity = Vector2(body.velocity.x, body.velocity.y * -diff)
    
#     # # # Collision X
#     # if abs(relPos.x) + body.radius > WIDTH:
#     #     normal = Vector2(utils.sign(relPos.x))
#     #     # print("Collide X")
        
#     #     if body.velocity > Vector2.zero:
#     #         diff = normal.dot(body.velocity.unit) * .4
            
#     #         # forceSum += gF * normal.dot(gF.unit)
#     #         for i in range(len(body.forces)):
#     #             force = body.forces[i]
#     #             if force.magnitude > 0:
#     #                 body.forces.append(force * normal.dot(force.unit) * 1.1)
            
#     #         body.velocity = Vector2(body.velocity.x * -diff, body.velocity.y)
            
    
#     if len(body.forces) != 0:
#         acc = vsum(body.forces)/body.mass * dt
#         body.accelerate(acc)
#         body.updatePos()