from .Deck import hand_out_cards


class Player:
    def __init__(self, deck):
        self.deck = deck
        self.hand = deck.hand_out_cards(6)

    def get_action(self, game_state):
        """
        calculate the appropriate action
        :param game_state:
        :return:
        """
