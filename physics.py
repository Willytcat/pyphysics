import math
import pygame
import utils
from time import time
from pyvectors import *
import drawer
import collision


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
    
    shape: drawer.Shape
    hitbox: collision.Collider
    
    
    def __init__(self, pos=Vector2(), vel=Vector2(), shape=None):
        self.position = pos
        self.velocity = vel
        self.shape = shape==None and shape or drawer.Circle(10)
        
        self.forces = []

    def __str__(self):
        return f"Body at {self.position}"

    
    def accelerate(self, dt):
        if len(self.forces) == 0: return

        # a = F/m
        acc = vsum(self.forces) / self.mass * dt
        self.velocity += acc
        self.position += self.velocity

    
    def translate(self, translation: Vector2):
        self.position += translation

    
    def rotate(self, radians: float):
        self.shape.rotate(radians)
    
    
    def draw(self, window):
        self.shape.draw(window, self.position)
    
    def getRelativePos(self, surfaceSize: Vector2):
        return self.position - surfaceSize/2


# Controller (adds controll other phy sim)
# RigidBody (adds local gravity simulation)
# Collider (adds collision detection and phy simulation)
# ForceField (adds force field force to other objects)
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
        # self._phyBodies = list(self.bodies)

        now = time()
        self.lastCall = now

        return now - self.lastCall
    
    def step(self) -> float:
        dt = self.newStep()

        for i, body in enumerate(self.bodies):
            # sim._phyBodies.pop()
            body.forces.clear()
            self.simulate(body, dt)
        

    def simulate(self, body: Body, dt):
        if body.anchored: return

        windowSize = Vector2(self.window.get_size())
        relPos = body.getRelativePos(windowSize)

        if self.gravityDir.magnitude > 0:
            g = body.mass * self.G
            body.forces.append(g * self.gravityDir)

        for other in self.bodies:
            if other == body: continue

            distance = other.position - body.position
            # penetrationDepth = body.radius + other.radius - distance.magnitude

            # if penetrationDepth > 0 and distance.magnitude != 0:
            #     print("Collision", time())
            #     normal = distance.unit

            #     other.color = Color("red")

            #     body.position -= normal * penetrationDepth

            #     # bounce = 0.8
            #     # if body.velocity > Vector2.zero:
            #     #     body.velocity *= -bounce*normal
                
            #     # # for force in body.forces:
            #     # #     if force.magnitude > 0:
            #     # #         diff = normal.dot(force.unit)
            #     # #         if diff < 0:
            #     # #             body.forces.append(force * normal.dot(force.unit) * penetrationDepth)
            # else:
            #     other.color = Color("white")

            if distance.magnitude != 0:
                direction = distance.unit
                attractionForce = self.GC*(body.mass*other.mass / distance.magnitude**2)

                body.forces.append(attractionForce*direction)
                # other.forces.append(-attractionForce*direction)


        for i, comp in enumerate(relPos.components):
            windowComp = windowSize.components[i]

            if abs(comp) + body.shape.radius > windowComp/2:
                # print(f"Border collision {i==0 and 'X' or 'Y'}")
                normal = i==0 and Vector2(-utils.sign(comp)) or Vector2(0, -utils.sign(comp))
                penetrationDepth = (abs(comp) + body.shape.radius - windowComp/2) / body.penetrationAcceptance

                if penetrationDepth > body.penetrationAcceptance:
                    body.position += normal * penetrationDepth

                if body.velocity > Vector2.zero:
                    borderBounce = utils.sign(normal.dot(body.velocity)) * 0.4
                    body.velocity *= i==0 and Vector2(borderBounce, 1) or Vector2(1, borderBounce)
                
                for force in body.forces:
                    if force.magnitude > 0:
                        diff = normal.dot(force.unit)
                        if diff < 0:
                            body.forces.append(force * normal.dot(force.unit) * penetrationDepth)
            
        body.accelerate(dt)


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