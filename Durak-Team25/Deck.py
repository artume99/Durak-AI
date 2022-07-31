from random import shuffle
from Card import Card


class Deck:
    def __init__(self):
        self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.ranks = list(range(2, 15))
        self.cards_list = []
        self.uber = None
        self.top_card = None
        self.build()

    def build(self):
        for s in self.suits:
            for r in self.ranks:
                self.cards_list.append(Card(r, s))
        self.shuffle()
        self.flip_top_card()

    def flip_top_card(self):
        # To be called at the start of the game, before cards are dealt
        self.top_card = self.pop()
        self.uber = self.top_card.suit
        for c in self.cards_list:
            c.uber = self.uber
        self.cards_list.insert(0, self.top_card)

    def shuffle(self):
        shuffle(self.cards_list)

    def pop(self):
        return self.cards_list.pop()

    def __len__(self):
        return len(self.cards_list)

    def __str__(self):
        return "Deck has {} cards left".format(len(self.cards_list))
