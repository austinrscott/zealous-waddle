from random import triangular

class Song:
    '''
    Songs have a few simple attributes.
    '''

    def __init__(self, quality, style, author):
        self.quality = quality
        self.style = style
        self.size = triangular(3, 12, 6)
        self.cost = 1.00
        self.author = author