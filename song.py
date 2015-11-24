from random import triangular


class Song:
    '''
    Songs have a few simple attributes.
    '''

    def __init__(self, quality, style):
        self.quality = quality
        self.style = style
        self.size = triangular(3, 12, 6)
