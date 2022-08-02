from .Deck import hand_out_cards
from .Game import Agent


class Player(Agent):
    def __init__(self, deck):
        super().__init__()
        self.deck = deck
        self.hand = deck.hand_out_cards(6)

    def get_action(self, game_state):
        """
        calculate the appropriate action
        :param game_state:
        :return:
        """
        pass


class Algo1(Player):
    def __init__(self, deck):
        super().__init__(deck)

    def get_action(self, game_state):
        """
        calculate the appropriate action
        :param game_state:
        :return:
        """
        pass
