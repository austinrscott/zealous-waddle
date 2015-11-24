class Site:
    def __init__(self):
        self.users = {}
        self.songs = []
        self.figures = {
            'sales': 0,
            'sales_dollars': 0,
            'plays': 0,
            'plays_mbs': 0,
            'previews': 0,
            'downloads': 0,
            'downloads_mbs': 0,
            'uploads_mbs': 0,
            'musician_payouts': 0,
            'promoter_payouts': 0,
            'site_fees': 0
        }
        self.settings = {
            'site_fee': 0.15,
            'musician_rate': 0.3,
            'promoter_rate': 0.7,
            'upline_rate': 0.6
        }

    def add_song(self, song, author):
        self.songs.append(song)
        self.figures['uploads_mbs'] += song.size

    def add_user(self, user):
        self.users[user] = {
            'income': 0,
            'songs': {},
        }

    def play_song(self, song):
        self.figures['plays'] += 1
        self.figures['plays_mbs'] += song.size

    def download_song(self, song):
        self.figures['downloads'] += 1
        self.figures['downloads_mbs'] += song.size

    def preview_song(self, song):
        self.figures['previews'] += 1
        self.figures['downloads_mbs'] += 1

    def sale(self, song, promoter, buyer):
        self.figures['site_fees']
        self.figures['promoter_payouts']
        self.figures['musician_payouts']
        self.users[promoter]['income'] +=
        # TODO: Finish sale function

    def commission_chain(self, song, ):
        # TODO: Finish recursive commission chain function

_site = Site()
