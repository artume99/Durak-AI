import abc

import pygame
import numpy as np
from Deck import Deck
from Board import Board
from Player import Player
from typing import List
from types import FunctionType


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
    def __init__(self):
        self.deck = Deck()
        self.board = Board()
        self.player = Player(self.deck)
        self.opponent = RandomOpponentAgent()
        self._should_quit = False
        self._state = None

    def run(self, initial_state):
        self._should_quit = False
        self._state = initial_state
        # self.display.initialize(initial_state)
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.agent.stop_running()
        self.opponent_agent.stop_running()

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
                6 - len(self.player.hand))
            self.opponent.hand += self.deck.hand_out_cards(
                6 - len(self.opponent.hand))
        else:
            self.opponent.hand += self.deck.hand_out_cards(
                6 - len(self.opponent.hand))
            self.player.hand += self.deck.hand_out_cards(
                6 - len(self.player.hand))

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

    def other_player(self, player):
        """
        returns they opponent of given player
        :param player:
        :return:
        """
        if player == self.player:
            return self.player
        return self.opponent

    def _game_loop(self):
        attacker = self.first_attacker()

        while not self._state.done and not self._should_quit:
            action = attacker.get_action(self._state)

            # check type of action like this
            # is there any point in having an "apply action" function?
            if action == Agent.place_card:
                pass
            if action == Agent.take:
                attacker = self.other_player(attacker)  # this will cause a player to have 2 turns in a row

            action = self.other_player(attacker).get_action(self._state)
            # now check action again with if's

            self.replenish_cards(attacker)
        # while not self._state.done and not self._should_quit:
        #     # self.display.mainloop_iteration()
        #     action = self.agent.get_action(self._state)
        #     # if action == Action.STOP:
        #     #     return
        #     self._state.apply_action(action)
        #     opponent_action = self.opponent_agent.get_action(self._state)
        #     self._state.apply_opponent_action(opponent_action)
        #     # self.display.update_state(self._state, action, opponent_action)
        #     self._state.update_state()
        #     self.hand_out_cards()
        # return self._state.score, self._state.max_tile
