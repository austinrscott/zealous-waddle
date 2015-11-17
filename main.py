import random

class Site:
    def __init__(self):

        # Initialize empty lists to hold users and songs
        self.users = list()
        self.songs = list()

        # Keeps track of site stats
        self.stats = {

            # This keeps track of total amount stored, and also how many mbs per day have been used since the beginning
            "mbs_storage": 0,
            "days_per_mbs_used": 0,

            # Bandwidth costs
            "mbs_upload": 0,
            "mbs_download": 0,

            # Users
            "total_users": 0,
            "musicians": 0,
            "promoters": 0,
            "fans": 0,
            "songs": 0,

            # Finances
            "gross_sales": 0,
            "musician_payouts": 0,
            "promoter_payouts": 0
        }

        self.launch(300)

    def launch(self, num_musicians):
        for i in range(num_musicians):
            self.users.append(Musician())

def nv(mu, sigma, low_cut, high_cut):
    #This helps to filter out random values we don't want.
    #It uses the normal variate function of the random library.
    a = -1
    while (a < low_cut) or (a > high_cut):
        a = random.normalvariate(mu, sigma)
    return a

def test(percent_chance):
    return (random.random() <= percent_chance)

class User:
    def __init__(self, *arg):
        if len(arg) == 0:
            a = self
        else:
            a = arg[0]
        a.library = list()
        a.audience = round(nv(400, 250, 0, 2000)) #random number near 400
        a.popularity = nv(0.075, 0.1, 0.001, 1) #percent chance audience reacts to thing
        a.sharer = nv(0.25, 0.25, 0, 1) #percent chance this person will decide to share something they buy
        a.sense = nv(0.3, 0.1, 0.05, 0.95) #percent chance this person recognizes song quality
        a.pickiness = nv(0.8, 0.2, 0.2, 1.9) #cutoff for what quality of song they will buy

class Musician(User):
    def __init__(self):
        super().__init__(self)
        self.skill = nv(0.5, 0.15, 0, 1) #adds to the quality of tracks
        self.talent = nv(0.5, 0.25, 0, 1) #a random modifier is added to every track, limited by talent
        self.writing_frequency = round(nv(60, 60, 1, 730)) #how many days, on average, before new material is released
        self.starting_set = round(nv(3, 1, 1, 8)) #how many songs the Musician has in the beginning of his signup

class Song:
    def __init__(self, creator, quality):
        self.creator = creator
        self.quality = quality

site = Site()