import random
import math

class Clock:
    '''Clock class keeps time for the simulation, measured in days. When tick() is called, it goes through the list of
    all time-based actors in the simulation and sends them tick() with the current time'''
    def __init__(self):
        self.time = 0
        self.ticking = []

    def tick(self):
        self.time += 1
        for actor in self.ticking:
            actor.tick(self.time)

    def add(self, *args):
        self.ticking.extend(args)

_clock = Clock()

class People:
    '''
    Keeps track of all of the people who exist in a different way than the site does. This tries to make networks
    organic outside of the site itself, to see what patterns emerge.
    '''
    pass

_people = People()

class MetaUser:
    '''This generates the stats that all users and people groups have.'''
    def __init__(self):
        self.charisma = random.random()
        self.sense = random.random()
        self.intelligence = random.random()
        self.talent = abs(random.normalvariate(0, 2/3))
        self.style = random.normalvariate(0.5, 1/6)
        self.pickiness = random.normalvariate(0.7, 1/3)
        self.sharer = random.random()

class PeopleGroup(MetaUser):
    '''This is used to simulate small subcultures of friends in which similar tastes are shared. This allows for some
    abstraction of groups of people.'''
    def __init__(self):
        super().__init__()
        self.diversity = random.triangular(0, 1, 0.25)

class User(MetaUser):
    '''Users are initiated with a boolean, if the boolean is True then the user is always a musician, otherwise it is a
    random chance.'''
    def __init__(self, boolean):
        super().__init__()

        self.library = []
        _clock.add(self)

        # Statista.com says that 18.08% of people played an instrument. I'd say that maybe a sixth of them make tracks
        if boolean == True or random.random() < 0.03:
            self.producer = True

            # Sets up the timer when this user will write a new song
            self.period = abs(random.normalvariate(90, 45)) * (1 + self.pickiness - self.talent)
            self.deviance = random.random() * self.period

            # Starting number of songs
            starting_set = round(random.random() * 4 + 2)
            for i in range(starting_set):
                self.write()
        else:
            self.producer = False

        self.audience = round(random.normalvariate(400, 100) * (1 + self.charisma))

    def reset_song_timer(self):
        self.next_song = abs(random.normalvariate(self.period, self.deviance))

    def write(self):
        base_quality = random.random() * 0.5
        mini = self.sense * 0.25
        maxi = self.intelligence * 0.25
        midpoint = maxi - mini * self.charisma
        musician_quality_mods = random.triangular(mini, maxi, midpoint)
        new_song = Song(base_quality + musician_quality_mods, self.style)
        self.library.append(new_song)
        self.share(new_song)
        self.reset_song_timer()

    def share(self, song):


    def appraise(self, song):
        roll = random.normalvariate(0.5, 0.153) * (1 + self.sense)
        if roll >= 0.95:
            return song.quality
        else:
            fail_margin = 0.95 - roll
            return random.normalvariate(song.quality, fail_margin / 3)

    def tick(self, time):
        if self.producer:
            self.next_song -= 1
            if self.next_song == 0:
                self.write()

class Song:
    '''
    Songs have a few simple attributes.
    '''
    def __init__(self, quality, style):
        self.quality = quality
        self.style = style
        self.size = random.normalvariate(7.75,1.25)

class Site:
    def __init__(self):
        self.users = []
        for i in range(500):
            self.users.append(User(True))

_site = Site()
print("Finished")