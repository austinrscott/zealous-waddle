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

class User:
    def __init__(self, upline):
        self.stats = UserStats()

class UserStats():
    def __init__(self):
        pass

class Stat():
    def __init__(self, mu, sigma, min, max):
        pass

class Song:
    def __init__(self, creator, quality):
        self.creator = creator
        self.quality = quality

site = Site()