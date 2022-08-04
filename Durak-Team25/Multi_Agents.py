# from .Deck import hand_out_cards
from .Game import Agent


class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    TAKE = 'a'
    PLACE_CARD = 'w'
    SWIPE_RIGHT = 'd'

    def __init__(self):
        super().__init__()

    def print_card(self, card):
        """
        prints something like 3DIAMOND...
        :param card:
        :return:
        """
        print(str(card.rank) + "" + str(card.suit))

    def get_action(self, state):
        selected_card_ind = 0
        print("your hand: ")
        for i in self.hand:
            self.print_card(i)
            print(" ")
        print("\ncurrently selected card: ")
        self.print_card(self.hand[selected_card_ind])
        inp = input("\ntake: a, place_card: w, swipe_right: d\n")

        while inp == "d":
            selected_card_ind += 1
            if selected_card_ind >= len(self.hand):
                selected_card_ind = 0
            print("currently selected card: ")
            self.print_card(self.hand[selected_card_ind])
            inp = input("\ntake: a, place_card: w, swipe_right: d\n")

        if inp == "a":
            self.hand += state.deck.beta_cards
            state.deck.beta_cards = []
        else:  # input == "w"
            state.deck.beta_cards += self.hand[selected_card_ind]
            self.hand.remove(self.hand[selected_card_ind])

    def stop_running(self):
        self._should_stop = True


class ExpectimaxAgent(Agent):
    def __init__(self, initial_cards=None):
        super().__init__(initial_cards)

    def get_action(self, game_state):
        """
        calculate the appropriate action
        :param game_state:
        :return:
        """
        pass
