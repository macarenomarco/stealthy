import sys
import math
import random

from kivy.vector import Vector

class Node(object):

    def __init__(self, data=None, parent=None, children=None):
        if not parent:
            self.parent = []
        else:
            self.parent = parent
        if not children:
            self.children = []
        else:
            self.children = children
        if not data:
            self.data = Vector(0.0, 0.0)
        else:
            self.data = data

class World(object):

    def __init__(self):
        self.player = None
        self.obstacles = []
        self.agents = []
        self.lastKnownPosition = Vector()
        pass

    def obstacleFun(self, p):
        for(obs in self.obstacles):
            if (obs.contains(p)):
                return float("inf")
        return 0.0

    def clearSight(self, a, b):
        for(obs in self.obstacles):
            if (obs.crosses(a, b)):
                return 0.0
        return 1.0

class Player(object):

    def __init__(self, world):
        self.world = world
        world.player = self
        self.pos = Vector(0.0, 0.0)

class Agent(object):

    def __init__(self, world, hearingRadio, minDistance):
        self.world = world
        self.pos = Vector(0.0, 0.0)
        self.minDistance = minDistance
        self.path = []
        self.hearingRadio = hearingRadio
        self.maxSeeing = 400
        self.visionAngle = 45
        self._rot = 0.0
        self.direction = [0, 0]

    @property
    def rotation(self):
        return self._rot

    @property.setter
    def rotation(self, value):
        if value > 360:
            value = value % 360
        self.direction = Vector(math.degrees(math.cos(math.radians(value))), math.degrees(math.sin(math.radians(value))))
        self._rot = value

    def listen(self):
        d = self.pos.distance(self.world.player.pos)
        if d < self.hearingRadio:
            self.world.lastKnownPosition = self.world.player.pos

    def see(self):
        if self.pos.distance(self.world.player.pos) and
            self.world.clearSight(self.pos, self.world.player.pos) and
            self.pos.distance(self.world.player.pos) < self.maxSeeing
            angle = Vector(self.direction - self.pos).angle(self.world.player.pos - self.pos)
            if  angle < self.visionAngle
                self.world.lastKnownPosition = self.world.player.pos

    def astar(self, p):
        return p.distance(elf.world.lastKnownPosition) + self.h(p)

    def h(self, p):
        return 0.0

    def calculatePath(self, next):
        if not next or next.distance(elf.world.lastKnownPosition) <= self.minDistance:
            return next
        return self.calculatePath(min(map(lambda p: self.astar(p.data), next.children)))

class AttackAgent(Agent):
    
    MIN_DISTANCE = 100

    def __init__(self, aggressiveness, hearingRadio, world):
        super(AttackAgent, self).__init__(world, hearingRadio, AttackAgent.MIN_DISTANCE)
        self.aggressiveness = aggressiveness

    @override
    def h(self, p):
        return -self.aggressiveness * self.world.clearSight(p, self.world.lastKnownPosition)

class SupportAgent(Agent):

    MIN_DISTANCE = 250

    def __init__(self, aggressiveness, hearingRadio, world):
        super(SupportAgent, self).__init__(world, hearingRadio, SupportAgent.MIN_DISTANCE)
        self.aggressiveness = aggressiveness

    @override
    def h(self, p):
        return -self.aggressiveness * self.world.clearSight(p, self.world.lastKnownPosition)

class Surround(Agent):

    MIN_DISTANCE = 100

    def __init__(self, stealth, hearingRadio, world):
        super(Surround, self).__init__(world, hearingRadio, Surround.MIN_DISTANCE)
        self.stealth = stealth

    @override
    def h(self, p):
        return stealth * self.world.clearSight(p, self.world.lastKnownPosition)