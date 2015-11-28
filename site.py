# TODO: Comment this file

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
            'musician_fee': 0.25,
            'upline_ratio': 0.6,
        }

    def add_song(self, song, author):
        self.songs.append(song)
        self.users[author]['songs'][song] = author
        self.figures['uploads_mbs'] += song.size

    def add_user(self, user):
        self.users[user] = {
            'income': 0,
            'expenses': 0,
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

    def buy_song(self, song, promoter, buyer):
        balance = self.exchange(song, promoter, buyer)
        balance -= self.pay_site()
        balance -= self.pay_musician(song.author)
        self.commission_chain(song, promoter, balance)

    def exchange(self, song, promoter, buyer):
        self.users[buyer]['expenses'] += song.cost
        self.users[buyer]['songs'][song] = promoter
        self.figures['sales'] += 1
        self.figures['sales_dollars'] += song.cost
        return song.cost

    def pay_site(self):
        self.figures['site_fees'] += self.settings['site_fee']
        return self.settings['site_fee']

    def pay_musician(self, musician):
        self.users[musician]['income'] += self.settings['musician_fee']
        self.figures['musician_payouts'] += self.settings['musician_fee']
        return self.settings['musician_fee']

    def pay_promoter(self, promoter, amount):
        upline_slice = amount * self.settings['upline_ratio']
        self.users[promoter]['income'] += amount - upline_slice
        self.figures['promoter_payouts'] += amount - upline_slice
        return upline_slice

    def commission_chain(self, song, promoter, balance):
        if promoter is song.author:
            self.users[song.author]['income'] += balance
            self.figures['musician_payouts'] += balance
        else:
            new_balance = self.pay_promoter(promoter, balance)
            self.commission_chain(song, self.users[promoter]['songs'][song], new_balance)