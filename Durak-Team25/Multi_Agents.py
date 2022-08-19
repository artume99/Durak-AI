import pygame

from GameState import GameState
from Game import Agent, Action
from pygame.locals import (
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)
from Constants import *

class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """

    # TAKE = 'down'
    # PLACE_CARD = 'space'
    # SWIPE_RIGHT = 'right'
    # SWIPE_LEFT = 'left'
    # BETA = 'up'

    def __init__(self):
        super().__init__()

    def get_action(self, state: GameState):
        print(f'kozer: {state.deck.kozer}, cards on board:{state.cards_on_board}')
        if state.card_in_play:
            print("Opponent played: ", end="")
            print(state.card_in_play)
        print("your hand: ")
        for card in self.hand:
            print(f'{card} ', end="")
        print("\ncurrently selected card: ", end="")
        print(self.hand[self.selected_card_ind])
        actions = state.get_legal_actions(0)
        print(f'You can play {actions}')
        print(MSG_FOR_KEYBOARD_AGENT)

        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            # if event.type == QUIT:
            #     pygame.quit()
            #     sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    card = self.hand[self.selected_card_ind]
                    self.selected_card_ind = 0
                    return card
                elif event.key == K_DOWN:
                    self.selected_card_ind = 0
                    return Action.TAKE
                elif event.key == K_UP:
                    self.selected_card_ind = 0
                    return Action.BETA
                elif event.key == K_RIGHT:
                    self.selected_card_ind += 1
                    if self.selected_card_ind >= len(self.hand):
                        self.selected_card_ind = 0
                        # state.draw_players(state.screen)
                    print("currently selected card: ", end="")
                    print(self.hand[self.selected_card_ind])
                    print(MSG_FOR_KEYBOARD_AGENT)
                    return Action.SWIPE
                elif event.key == K_LEFT:
                    self.selected_card_ind -= 1
                    if self.selected_card_ind < 0:
                        self.selected_card_ind = len(self.hand) - 1
                        print("currently selected card: ", end="")
                        print(self.hand[self.selected_card_ind])
                        print(MSG_FOR_KEYBOARD_AGENT)
                    return Action.SWIPE

        # inp = pygame.key.get_pressed()
        # while True:
        #     while inp[K_RIGHT]:
        #         selected_card_ind += 1
        #         if selected_card_ind >= len(self.hand):
        #             selected_card_ind = 0
        #         print("currently selected card: ", end="")
        #         print(self.hand[selected_card_ind])
        #         print("\ntake: up, place_card: left, swipe_right: right, beta: down\n")
        #         inp = pygame.key.get_pressed()
        #     if inp[K_LEFT] or inp[K_UP]:
        #         break
        #
        # if inp[K_LEFT]:
        #     return Action.TAKE
        # elif inp[K_UP]:
        #     return self.hand[selected_card_ind]
        # else:
        #     return Action.BETA

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
