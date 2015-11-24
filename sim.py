from random import normalvariate as nv


class Sim:
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


def add_to_tick(new_actor):
    simulation.add(new_actor)


def filter_nv(mu, sigma):
    result = -1
    while result < 0 or result > 1:
        result = nv(mu, sigma)
    return result


def calc_proximity(entity_a, entity_b):
    proximity = 1 - abs(entity_a.style - entity_b.style)
    return proximity


simulation = Sim()
