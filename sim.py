import math
from random import normalvariate as nv

from people import People
from site import Site

# TODO: Comment this file

print("IMPORTING SIM".center(80, '-'))

class Clock:
    '''Clock class keeps time for the simulation, measured in days. When tick() is called, it goes through the list of
    all time-based actors in the simulation and sends them tick() with the current time'''

    def __init__(self):
        self.time = 0
        self.tick_list = []

    def tick(self):
        self.time += 1
        for actor in self.tick_list:
            actor.tick(self.time)

    def add(self, *args):
        self.tick_list.extend(args)

def filter_nv(mu, sigma):
    result = -1
    while result < 0 or result > 1:
        result = nv(mu, sigma)
    return result

def calc_proximity(entity_a, entity_b):
    proximity = math.sqrt((entity_a.style[0] - entity_b.style[0]) ** 2 + (entity_a.style[1] - entity_b.style[1]) ** 2)
    return proximity


clock = Clock()
site = Site()

# Functions for the module to interface with outside modules

def add_to_tick(new_actor):
    clock.add(new_actor)

def populate(num_people, num_musicians):
    global people
    people = People(num_people, num_musicians)

def terminate():
    print("END OF TEST".center(80, '-'))
