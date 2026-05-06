import pygame
import physics as phy
from copy import deepcopy
from pyvectors import *
import drawer


distorderBodyDescr = {
    "anchored": True,
    "exerceForce": True,
    "mass": 100
}

plr = phy.Body()
plr.anchored = True
plr.exerceForce = False
plr.mass = 10

exitBody = phy.Body()
exitBody.anchored = True
exitBody.exerceForce = False
exitBody.shape.color = (0, 255, 255)

sim_bodies = []
phySimulation = phy.Simulation(sim_bodies)


def start():
    loadLevel(1)

    return True

def loadLevel(id: int):
    if 0 < id < len(levels) - 1:
        raise OverflowError("level id out of range")

    level = levels[id]
    sim_bodies.clear()

    maxBodies = level["maxBodies"]

    plr.anchored = True
    plr.position = level["plrPos"]
    exitBody.position = level["exitPos"]
    
    sim_bodies.append(plr)
    sim_bodies.append(exitBody)

    for descr in level["bodies"]:
        sim_bodies.append(loadPhyBody(descr))


def nextLevel():
    currentLevel = (currentLevel + 1) % len(levels)
    loadLevel(currentLevel)


def restartLevel():
    loadLevel(currentLevel)


def addDistorderAt(at: Vector2):
    newBody = loadPhyBody(distorderBodyDescr)
    newBody.position = at

    sim_bodies.append(newBody)


def loadPhyBody(descr: dict):
    body = phy.Body()

    for attr, value in descr.items():
        setattr(body, attr, value)

    return body


def prePhysics(dt: float):
    mouseInputs = pygame.mouse.get_pressed()

    if mouseInputs[0]:
        mousePosition = Vector2(pygame.mouse.get_pos())
        distance = mousePosition - plr.position
        force = -2*distance

        plr.forces.append(force)



windowSize = Vector2(800, 800)

maxBodies = 99999
currentLevel = 0

levels = [
    {
        "maxBodies": 99999, 
        "bodies": [],

        "plrPos": Vector2(),
        "exitPos": Vector2(windowSize.x-50, windowSize.y/2)
    },
    {
        "maxBodies": 3, 
        "bodies": [
            {"position": windowSize/2, "mass": 1e8, "anchored": True, "shape": drawer.Circle(80)}
        ],

        "plrPos": Vector2(),
        "exitPos": Vector2(windowSize.x-30, windowSize.y/2)
    }
]

keyBinds = {
    97: {
        "type": "action",
        "callback": addDistorderAt, 
        "requiredData": ["mousePosition"]
        },
    114: {
        "type": "action",
        "callback": restartLevel,
        "requiredData": []
    },

    27: {
        "type": "specialAction",
        "action": "exit"
    }
}
