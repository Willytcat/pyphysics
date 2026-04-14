import math
import pygame
from time import time
from pyvectors import *
class Body():
    position: Vector2
    velocity: Vector2
    mass: int = 1
    forces: list
    anchored : bool = False
    exerceForce: bool = False
    canCollide: bool = True
    radius: float = 10
    color: tuple = (255, 255, 255)
    
    
    def __init__(self, pos, vel=Vector2(), color=None, radius=None):
        self.position = pos
        self.velocity = vel
        
        if color is not None:
            self.color = color
        if radius is not None:
            self.radius = radius
        
        self.forces = []
        
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

class Simulation():
    window: pygame.Surface
    lastCall: float
    
    
    bodies: [Body]
    _phyBodies: [Body]
    G = 9.81
    GC = 6.67
    gravityDir: Vector2
    def __init__(self, bodies):
        bodies = bodies
    def step(self):
        self.phy_bodies = list(self.bodies)
        
        
        for body in self.bodies:
            self.simulate(body)
    def simulate(self, body: Body):
        if body.anchored: return

        

def step(sim: Simulation):
    sim._phyBodies = list(sim.bodies)
    
    now = time()
    dt = now - sim.lastCall
    sim.lastCall = now
    for i, body in enumerate(self.bodies):
        sim._phyBodies.pop()
        
        simulate(sim, body, dt)


def simulate(sim: Simulation, body: Body, dt=None):
    if dt is None:
        now = time()
        dt = now - sim.lastCall
        sim.lastCall = now

    if body.anchored: return
    relPos = body.getRelativePos(sim.window.get_size())
    
    if sim.gravityDir.magnitude > 0:
        g = body.mass * sim.G
        gF: Vector2 = g * gravityDir
        body.forces.append(gF)
        # forceSum += gF
    
    for other in _phyBodies:
        # Continues if no interactions between bodies
        if not body.exerceForce and not other.exerceForce: continue
        
        distance = body.position - other.position
        
        if distance.magnitude-body.radius-other.radius < 0 and body.canCollide and other.canCollide:
            print('collision')
        if distance.magnitude != 0:
            direction = distance.unit
            bodyGF = GC*(body.mass*other.mass / distance.magnitude**2)
            
            # other exerce a force on body
            if other.exerceForce:
                body.forces.append(bodyGF*direction)
            
            # body exerce a force on other if other is not anchored
            if body.exerceForce and not other.anchored:
                other.forces.append(-bodyGF*direction)

        
    
    
    if mouseInput[0] or mouseInput[2]:
        forceType = mouseInput[0] and 1 or -1
        distance = body.position - mousePos
        if distance.magnitude < 1e4:
            body.forces.append(forceType * distance.unit * 3e4/distance.magnitude)
            # forceSum += -(body.position - mousePos).unit * 10
    
    
    # Collision Y
    if abs(relPos.y) + body.radius > HEIGHT:
        normal = Vector2(0, utils.sign(relPos.y))
        # print("COllide Y")
        if body.velocity > Vector2.zero:
            diff = normal.dot(body.velocity.unit) * .4
            
            # forceSum += gF * normal.dot(gF.unit)
            for i in range(len(body.forces)):
                force = body.forces[i]
                if force.magnitude > 0:
                    body.forces.append(force * normal.dot(force.unit)* 1.1)
            
            body.velocity = Vector2(body.velocity.x, body.velocity.y * -diff)
    
    # # Collision X
    if abs(relPos.x) + body.radius > WIDTH:
        normal = Vector2(utils.sign(relPos.x))
        # print("Collide X")
        
        if body.velocity > Vector2.zero:
            diff = normal.dot(body.velocity.unit) * .4
            
            # forceSum += gF * normal.dot(gF.unit)
            for i in range(len(body.forces)):
                force = body.forces[i]
                if force.magnitude > 0:
                    body.forces.append(force * normal.dot(force.unit) * 1.1)
            
            body.velocity = Vector2(body.velocity.x * -diff, body.velocity.y)
            
    
    if len(body.forces) != 0:
        acc = vsum(body.forces)/body.mass * dt
        body.accelerate(acc)
        body.updatePos()