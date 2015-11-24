from random import normalvariate as nv, random, triangular

import sim
import song

class People:
    '''
    Keeps track of all of the people who exist in a different way than the site does. This tries to make networks
    organic outside of the site itself to see what patterns emerge.
    '''

    def __init__(self, num_musicians_desired):
        self.people = []
        self.groups = []
        self.groups.append(PeopleGroup(num_musicians_desired, True))

class Person:
    '''This generates the stats that all users and people groups have.'''

    def __init__(self, stats=None):
        if stats == None:
            self.initialize_stats()
        else:
            self.stats = stats
        self.reset_stats()

    def initialize_stats(self):
        self.stats = self.population_template()
        self.reset_stats()

    def population_template(self):
        stats = {
            'charisma': random(),
            'sense': random(),
            'intelligence': random(),
            'talent': sim.filter_nv(0, 2 / 3),
            'style': sim.filter_nv(0.5, 1 / 6),
            'pickiness': sim.filter_nv(0.8, 1 / 3),
            'sharer': random()
        }
        return stats

    def reset_stats(self):
        for stat in self.stats.keys():
            setattr(self, stat, self.stats[stat])

    def show_stats(self):
        return self.stats

    def appraise(self, song):
        roll = sim.filter_nv(0.5, 0.153) * (1 + self.sense)
        if roll >= 0.95:
            return song.quality
        else:
            fail_margin = 0.95 - roll
            return sim.filter_nv(song.quality, fail_margin / 3)

    def like(self, song):
        proximity = sim.calc_proximity(self, song)
        if proximity > self.pickiness:
            return True
        else:
            return False

class User(Person):
    '''Users are initiated with a boolean, if the boolean is True then the user is always a musician, otherwise it is a
    random chance.'''

    def __init__(self, person=None):
        if person:
            super().__init__(person.stats)
        else:
            super().__init__()

        self.library = []
        self.audience = round(nv(400, 100) * (1 + self.charisma))

    def purchase(self, user, song):
        self.library.append(song)
        sim.initialize_sale(song, user)

    def share(self, song):
        pass

class Musician(User):
    def __init__(self):
        super().__init__()

        # Sets up the timer when this user will write a new song
        self.writing_period = abs(nv(90, 45)) * (1 + self.pickiness - self.talent)
        self.period_deviance = random() * self.writing_period

        # Adds the musician to the "tick" list
        sim.add_to_tick(self)

        # Starting number of songs
        starting_set = round(random() * 4 + 2)
        for i in range(starting_set):
            self.write()

    def reset_song_timer(self):
        self.next_song = round(abs(nv(self.writing_period, self.period_deviance)))

    def tick(self, time):
        self.next_song -= 1
        if self.next_song == 0:
            self.write()

    def write(self):
        base_quality = random() * 0.6
        mini = self.sense * 0.3
        maxi = self.intelligence * 0.3
        midpoint = maxi - mini * self.charisma
        musician_quality_mods = triangular(mini, maxi, midpoint)
        new_song = song.Song(base_quality + musician_quality_mods, self.style, self)
        self.library.append(new_song)
        self.share(new_song)
        self.reset_song_timer()

class PeopleGroup(Person, list):
    '''This is used to simulate small subcultures of people in which similar tastes are shared. This allows for some
    abstraction of groups of people.'''

    def __init__(self, population, launch_group=False):
        super(list).__init__()
        super(Person).__init__()
        if launch_group:
            '''The launch group is the target group created to launch the site. A diverse group of musicians, they each
                have their own audiences which assists in quick growth in the launch period.'''
            self.extend([Musician() for i in range(population)])
            self.diversity = 1
        else:
            # Statista.com says that 18.08% of people played an instrument. I'd say that maybe a sixth of them make tracks
            musicians = round(population * 0.03)
            listeners = population - musicians
            self.diversity = triangular(0.1, 0.9, 0.25)
            self.extend([Musician() for i in range(musicians)])
            self.extend([User() for i in range(listeners)])

    def apply_diversity(self, user):
        for statname, value in user.stats:
            user.stats[statname] = self.stats[statname] + (self.stats[statname] - value) * self.diversity