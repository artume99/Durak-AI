# from .Deck import hand_out_cards
from GameState import GameState
from Game import Agent, Action


class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    TAKE = 'a'
    PLACE_CARD = 'w'
    SWIPE_RIGHT = 'd'

    def __init__(self):
        super().__init__()

    def get_action(self, state: GameState):
        print(f'kozer: {state.deck.kozer}, cards on board:{state.cards_on_board}')
        if state.card_in_play:
            print("Opponent played: ", end="")
            print(state.card_in_play)
        selected_card_ind = 0
        print("your hand: ")
        for card in self.hand:
            print(f'{card} ', end="")
        print("\ncurrently selected card: ", end="")
        print(self.hand[selected_card_ind])
        actions = state.get_legal_actions(0)
        print(f'You can play {actions}')
        inp = input("\ntake: a, place_card: w, swipe_right: d, beta: b\n")
        while inp == "d":
            selected_card_ind += 1
            if selected_card_ind >= len(self.hand):
                selected_card_ind = 0
            print("currently selected card: ", end="")
            print(self.hand[selected_card_ind])
            inp = input("\ntake: a, place_card: w, swipe_right: d, beta: b\n")

        if inp == "a":
            return Action.TAKE
        elif inp == "w":
            return self.hand[selected_card_ind]
        else:
            return Action.BETA


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
