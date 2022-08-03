import abc
from enum import Enum

import pygame
import numpy as np
from Deck import Deck
from Board import Board
from typing import List
from types import FunctionType

from GameState import GameState
class Action(Enum):
    BETA = 0
    TAKE = 1
    STOP = 2

class Agent(object):
    def __init__(self, deck):
        super(Agent, self).__init__()
        self.deck = deck
        self.hand = deck.hand_out_cards(6)

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

    def place_card(self, card):
        pass

    def take(self):
        pass


class RandomOpponentAgent(Agent):
    """
    The opponent
    """
    def get_action(self, game_state):
        pass


class Game:
    def __init__(self, agent: Agent, opponent: Agent):
        self.deck = Deck()
        self.player = agent
        self.opponent = opponent
        self._should_quit = False
        self._state: GameState = GameState()

    def run(self, initial_state: GameState):
        self._should_quit = False
        self._state = initial_state
        # self.display.initialize(initial_state)
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.player.stop_running()
        self.opponent.stop_running()

    def replenish_cards(self, attacker):
        """
        check if either player needs more cards and give them if necessary
        the attacker gets cards first
        :return:
        """
        if len(self.deck.cards_list) <= 0:
            return
        if attacker == self.player:
            self.player.hand += self.deck.hand_out_cards(
                max(0, 6 - len(self.player.hand)))
            self.opponent.hand += self.deck.hand_out_cards(
                max(0, 6 - len(self.opponent.hand)))
        else:
            self.opponent.hand += self.deck.hand_out_cards(
                max(0, 6 - len(self.opponent.hand)))
            self.player.hand += self.deck.hand_out_cards(
                max(0, 6 - len(self.player.hand)))

    def first_attacker(self):
        """
        who attacks first on the start of the game
        :return:
        """
        chosen_shape = self.deck.top_card.suit
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

    def _game_loop(self):
        attacker = self.first_attacker()
        self._state.attacker = attacker
        self._state.defender = self.other_player(attacker)

        while not self._state.done and not self._should_quit:
            action = attacker.get_action(self._state)
            if action == Action.STOP:
                return
            self._state.apply_action(action)
            if action == Action.BETA:
                attacker = self.other_player(attacker)
                continue
            opponent_action = self.opponent.get_action(self._state)
            self._state.apply_opponent_action(opponent_action)
            self.replenish_cards(attacker)
            attacker = self.other_player(attacker)
        return self._state.winner
