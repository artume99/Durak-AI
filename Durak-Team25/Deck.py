import numpy as np
from Card import Card
from itertools import product


class Deck:
    """

    """

    def __init__(self):
        # self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.suits = ['♠', '♥', '♦', '♣']

        self.ranks = list(range(6, 15))  # not supposed to use 2-5 ranked cards
        self.cards_list, self.beta_cards = [], []
        self.kozer = None
        self.top_card = None
        # self.opened_cards = []
        # self.tossed_cards = []  # cards that have been deleted from the game
        self.build()

    def build(self):
        self.cards_list, self.beta_cards = [], []
        for s in self.suits:
            for r in self.ranks:
                self.cards_list.append(Card(r, s))
        self.shuffle()
        self.flip_top_card()

    def flip_top_card(self):
        # To be called at the start of the game, before cards are dealt
        self.top_card = self.pop()
        self.kozer = self.top_card.suit
        for card in self.cards_list:
            if card.suit == self.kozer:
                card.kozer = True
        self.cards_list.insert(0, self.top_card)  # should be the last card of the card list
        # self.opened_cards.insert(0, self.top_card)

    def shuffle(self):
        np.random.shuffle(self.cards_list)

    def pop(self):
        return self.cards_list.pop()

    def __len__(self):
        return len(self.cards_list)

    def __str__(self):
        return "Deck has {} cards left".format(len(self.cards_list))

    def hand_out_cards(self, num):
        """
        give a maximum of num cards
        :param num:
        :return:
        """
        cards_to_hand = []
        num_of_card_to_hand = min(num, len(self.cards_list))
        for i in range(num_of_card_to_hand):
            cards_to_hand.append(self.pop())
        return cards_to_hand

    def add_to_beta(self, cards):
        self.beta_cards.extend(cards)