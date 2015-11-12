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

    def launch(self, num_musicians):
        for i in range(num_musicians):
            self.users.append(Musician())

class User:
    def __init__(self):
        self.library = list()
        self.audience = 0#random number near 400
        self.popularity = #percent chance audience reacts to thing
        self.sharer = #percent chance this person will decide to share something they buy
        self.sense = #percent chance this person recognizes song quality

class Musician(User):
    def __init__(self):
        super().__init__(self)
        self.skill = #adds to the quality of tracks
        self.talent = #a random modifier is added to every track, limited by talent
        self.frequency = #how many days, on average, before new material is released
        self.starting_set = #how many songs the Musician has in the beginning of his signup
        pass