class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.kozer = False

    def is_kozer(self):
        return self.kozer