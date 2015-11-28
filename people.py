from random import normalvariate as nv, random, triangular, sample

import sim
import song


# TODO: Comment this file

class People:
    '''
    Keeps track of all of the people who exist in a different way than the site does. This tries to make networks
    organic outside of the site itself to see what patterns emerge.
    '''

    def __init__(self, population_desired, musicians_desired):
        self.groups = []
        while self.population() < population_desired or self.musicians() < musicians_desired:
            self.groups.append(PeopleGroup(round(triangular(10, 500, 200))))

    def population(self):
        return sum([len(x) for x in self.groups])

    def all_people(self):
        return list(*self.groups)

    def musicians(self):
        return sum([x.musicians for x in self.groups])

class Person:
    '''This generates the stats that all users and people groups have, without instantiating the actual classes used
    for the person. This assists in abstraction of large userbases.'''

    def __init__(self, stats=None):
        if stats == None:
            self.initialize_stats()
        else:
            self.stats = stats
        self.reset_stats()
        self.tags = {}
        self.audience = round(nv(400, 100) * (1 + self.charisma))
        self.friends = []

    def tag(self, **tags):
        self.tags.update(tags)

    def initialize_stats(self):
        self.stats = self.population_template()

    def population_template(self):
        stats = {
            'charisma': random(),
            'sense': random(),
            'intelligence': random(),
            'talent': sim.filter_nv(0, 2 / 3),
            'style': (sim.filter_nv(0.5, 1 / 6), sim.filter_nv(0.5, 1 / 6)),
            'pickiness': sim.filter_nv(0.8, 1 / 3),
            'sharer': random(),
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

    def like(self, song, charisma_modifier=0):
        proximity = sim.calc_proximity(self, song)
        if proximity > self.pickiness - charisma_modifier:
            return True
        else:
            return False

    def at_max_friends(self):
        if len(self.friends) < self.audience:
            return False
        else:
            return True

    def set_people_group(self, pg):
        self.people_group = pg

    def add_friend(self, other):
        if not self.at_max_friends() and not other.at_max_friends():
            self.friends.append(other)
            other.friends.append(self)
            return True

    def friendly(self, other):
        cha_diff = self.charisma - other.charisma
        if self.like(other, cha_diff) and other.like(self, -cha_diff):
            return True
        else:
            return False

    def decide_purchase(self, song, sharer):
        sim.site.preview_song(song)
        if self.like(song) and self.appraise(song) > self.pickiness:
            if not self.account:
                self.create_account()
            sim.site.buy_song(song, sharer, self)

    def get_muse(self):
        self.muse = Muse(self)

    def create_account(self):
        self.account = UserAccount(self)
        sim.site.add_user(self.account)
        self.people_group.remove(self)

    def share(self, song):
        pass


class UserAccount:
    def __init__(self, person):
        self.acct_holder = person
        self.library = []

    def purchase(self, user, song):
        self.library.append(song)
        sim.site.buy_song(song, user, self)


class Muse:
    def __init__(self, person):
        self.person = person

        # Links to Person's stat values.

        self.pickiness = person.pickiness
        self.talent = person.talent
        self.sense = person.sense
        self.intelligence = person.intelligence
        self.charisma = person.charisma
        self.style = person.style

        # Sets up the timer when this muse will generate a new song
        self.writing_period = abs(nv(90, 45)) * (1 + self.pickiness - self.talent)
        self.period_deviance = random() * self.writing_period

    def activate(self):
        # Adds the muse to the "tick" list
        sim.add_to_tick(self)

        # Starting number of songs
        starting_set = round(random() * 4 + 2)
        for i in range(starting_set):
            self.write()

    def reset_song_timer(self):
        self.next_song_countdown = round(abs(nv(self.writing_period, self.period_deviance)))

    def tick(self, time):
        self.next_song_countdown -= 1
        if self.next_song_countdown == 0:
            self.write()

    def write(self):
        base_quality = random() * 0.6
        mini = self.sense * 0.3
        maxi = self.intelligence * 0.3
        midpoint = maxi - mini * self.charisma
        musician_quality_mods = triangular(mini, maxi, midpoint)
        new_song = song.Song(base_quality + musician_quality_mods, self.style, self)
        self.person.account.library.append(new_song)
        sim.site.add_song(new_song, self)
        self.person.share(new_song)
        self.reset_song_timer()

class PeopleGroup(Person, list):
    '''This is used to simulate small subcultures of people in which similar tastes are shared. This allows for some
    abstraction of groups of people.'''

    def __init__(self, population):
        super(list, self).__init__()

        super(Person, self).__init__()
        # Statista.com says that 18.08% of people played an instrument. I'd say that maybe a sixth of them make tracks
        self.musicians = round(population * 0.03)
        self.listeners = population - self.musicians
        self.diversity = triangular(0.1, 0.9, 0.25)
        people = [Person() for x in range(population)]
        for person in people:
            self.apply_diversity(person)
            person.reset_stats()
            person.set_people_group(self)
        for musician in sample(self, self.musicians):
            musician.get_muse()

    def apply_diversity(self, user):
        for statname, value in user.stats.items():
            user.stats[statname] = self.stats[statname] + (self.stats[statname] - value) * self.diversity

    def tag(self, *targets, **tags):
        for target in targets:
            print("Trying to tag " + repr(target))
            target.tag(**tags)
