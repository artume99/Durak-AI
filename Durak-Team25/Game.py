import abc

import pygame
from Deck import Deck
from Board import Board
from Player import Player
from typing import List


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass


class RandomOpponentAgent(Agent):
    def get_action(self, game_state):
        pass


class Game:
    def __init__(self):
        self.deck = Deck()
        self.board = Board()
        self.player1 = Player()
        self.player2 = Player()
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

    def _game_loop(self):
        while not self._state.done and not self._should_quit:
            # self.display.mainloop_iteration()
            action = self.agent.get_action(self._state)
            # if action == Action.STOP:
            #     return
            self._state.apply_action(action)
            opponent_action = self.opponent_agent.get_action(self._state)
            self._state.apply_opponent_action(opponent_action)
            # self.display.update_state(self._state, action, opponent_action)
        return self._state.score, self._state.max_tile
