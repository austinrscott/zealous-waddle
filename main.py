class Site:
    def __init__(self):
        # Initialize empty lists to hold users and songs
        self.users = list()
        self.songs = list()

        # Keeps track of site stats
        stats = {
            "storage": 0,
            "users": 0,
            "musicians": 0,
            "songs": 0,
            "income": 0
        }