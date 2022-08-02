# from .Deck import hand_out_cards
from .Game import Agent


class Algo1(Agent):
    def __init__(self, deck):
        super().__init__(deck)

    def get_action(self, game_state):
        """
        calculate the appropriate action
        :param game_state:
        :return:
        """
        pass
