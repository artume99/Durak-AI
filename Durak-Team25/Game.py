import abc
from enum import Enum

import pygame
import numpy as np
from Card import Card
from Deck import Deck
from typing import List, Iterable
from types import FunctionType


class Action(Enum):
    BETA = 0  # might be multiple cards?
    TAKE = 1
    SWIPE = 2


class Agent(object):
    def __init__(self, initial_cards: List = None):
        super(Agent, self).__init__()
        self.hand = initial_cards
        self.selected_card_ind = 0

    @abc.abstractmethod
    def get_action(self, game_state) -> FunctionType:
        """
        return a function of an action
        :param game_state:
        :return:
        """
        return

    def stop_running(self):
        pass


class RandomOpponentAgent(Agent):
    """
    The opponent
    """

    def __init__(self, initial_cards=None, passive_action_weight=10, kozer_weight=10):
        super().__init__(initial_cards)
        self.passive_action_weight = passive_action_weight
        self.kozer_weight = kozer_weight

    def get_action(self, game_state):
        legal_actions = game_state.get_opponent_legal_actions()
        # weights = np.array(self._weight_actions(
        #     legal_actions)) / 100  # can be added as third param in the line below but seems uneeded
        action = np.random.choice(legal_actions, 1)[0]
        return action

    def _weight_actions(self, actions):
        weights = []
        # if there are a lot of action, each action which is not BETA, TAKE has a big value
        base_weight = len(actions) * 10
        for action in actions:
            if action in [Action.BETA, Action.TAKE]:
                weights.append(self.passive_action_weight)
            elif action.is_kozer():
                weights.append(self.kozer_weight)
            else:
                weights.append(base_weight)
        return weights


class Game:
    def __init__(self, agent: Agent, opponent: Agent):
        self.screen = None
        self.player = agent
        self.opponent = opponent
        self._should_quit = False
        self._state = None

    def run(self, initial_state, screen):
        self.screen = screen
        self._should_quit = False
        self._state = initial_state
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.player.stop_running()
        self.opponent.stop_running()

    def first_attacker(self):
        """
        who attacks first on the start of the game
        :return:
        """
        chosen_shape = self._state.deck.kozer
        min_rank = 15
        starting_attacking_player = self.player
        for card in self.player.hand:
            if card.suit == chosen_shape and card.rank < min_rank:
                starting_attacking_player = self.player
                min_rank = card.rank
        for card in self.opponent.hand:
            if card.suit == chosen_shape and card.rank < min_rank:
                starting_attacking_player = self.opponent
                min_rank = card.rank
        return starting_attacking_player

    def other_player(self, player: Agent):
        """
        returns the opponent of given player
        :param player:
        :return:
        """
        if player == self.player:
            return self.opponent
        return self.player

    def set_background(self):
        self.background = pygame.surface.Surface((800, 600))
        self.background.fill((7, 99, 36))
        self.screen.blit(self.background, (0, 0))

    def _game_loop(self):
        attacker = self.first_attacker()
        defender = self.other_player(attacker)
        self._state.attacker = attacker
        self._state.defender = defender

        while not self._state.done and not self._should_quit:
            self.set_background()
            self._state.render(self.screen)
            pygame.display.flip()
            pygame.display.update()

            action = self._state.attacker.get_action(self._state)
            self.render()
            # if action == Action.STOP:
            #     return
            while action is Action.SWIPE:
                action = self._state.attacker.get_action(self._state)
                self.render()

            self._state.apply_attack_action(action)
            if self._state.done:
                break
            if action in [Action.BETA, Action.TAKE]:
                continue
            self.render()

            opponent_action = self._state.defender.get_action(self._state)
            self.render()
            while opponent_action is Action.SWIPE:
                opponent_action = self._state.defender.get_action(self._state)
                self.render()

            self._state.apply_defend_action(opponent_action)

        return self._state.looser

    def render(self):
        self.set_background()
        self._state.render(self.screen)
        pygame.display.flip()
        pygame.display.update()
