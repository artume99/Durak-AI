class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.kozer = False

    def is_kozer(self):
        return self.kozer

    def __str__(self):
        return str(self.rank) + "" + str(self.suit)

    def __repr__(self):
        return str(self.rank) + "" + str(self.suit)
