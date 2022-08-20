import copy
from enum import Enum
from typing import Tuple

import numpy as np

from util import Counter

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


class AgentNum(Enum):
    Player = 0
    Computer = 1


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
        if len(self.hand) > 0:
            print(self.hand[self.selected_card_ind])
        actions = state.get_legal_actions(0)
        print(f'You can play {actions}')
        print(state.deck)
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


def get_hand_dicts(hand):
    card_ranks = Counter()
    card_suits = Counter()
    for card in hand:
        card_ranks[card.rank] += 1
        card_suits[card_suits] += 1
    return card_ranks, card_suits


def base_evaluation(game_state):
    if game_state.is_attacking(0):
        hand, op_hand = game_state.attacker.hand, game_state.defender.hand
    else:
        op_hand, hand = game_state.attacker.hand, game_state.defender.hand

    return len(op_hand) - len(hand)


class MultiAgentSearchAgent(Agent):
    def __init__(self, evaluation_function=base_evaluation, depth=2):
        super().__init__()
        self.evaluation_function = evaluation_function
        self.depth = depth

    def get_action(self, game_state: GameState):
        return


class ExpectimaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        expectimax = self.expctimax(game_state, self.depth, AgentNum.Player)
        return expectimax[1]

    def expctimax(self, game_state: GameState, depth: int, agent: AgentNum):
        # region End Condition
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region Expected Max
        if agent == AgentNum.Player:
            legal_moves = game_state.get_legal_actions(agent.value)
            max_val = (float("-inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent.value, move)
                response_val = self.expctimax(new_state, depth - 1, AgentNum.Computer)[0], move
                max_val = max(max_val, response_val, key=costume_key)
            return max_val

        # endregion

        # region Expected Min
        if agent == AgentNum.Computer:
            legal_moves = game_state.get_legal_actions(agent.value)
            succesors = []
            for move in legal_moves:
                succesors.append(game_state.generate_successor(agent.value, move))
            succesors = np.array(succesors)
            probability_s = 1 / len(succesors)
            vfunc_expectimax = np.vectorize(self.expctimax)
            responses = vfunc_expectimax(succesors, depth, agent.Player)
            expectation = np.sum(responses[0] * probability_s), Action.STOP
            return expectation

        # endregion
        return

    def copy(self):
        new_agent = ExpectimaxAgent()
        new_hand = []
        for card in self.hand:
            new_hand.append(card.copy())
        new_agent.hand = new_hand
        return new_agent


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state: GameState):
        minimax = self.minimax(game_state, self.depth, AgentNum.Player)
        return minimax[1]

    def minimax(self, game_state: GameState, depth: int, agent: AgentNum) -> Tuple[int, Action]:
        # region if 𝑑𝑒𝑝𝑡ℎ = 0 or v is a terminal node then return 𝑢(𝑣)
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region  if isMaxNode then return max
        if agent == AgentNum.Player:
            legal_moves = game_state.get_legal_actions(agent.value)
            max_val = (float("-inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent.value, move)
                response_val = self.minimax(new_state, depth - 1, AgentNum.Computer)[0], move
                max_val = max(max_val, response_val, key=costume_key)
            return max_val

        # endregion

        # region  if isMinNode then return min
        if agent == AgentNum.Computer:
            legal_moves = game_state.get_legal_actions(agent.value)
            min_val = (float("inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent.value, move)
                response_val = self.minimax(new_state, depth, AgentNum.Player)[0], move
                min_val = min(min_val, response_val, key=costume_key)
            return min_val
        # endregion

    def copy(self):
        new_agent = MinmaxAgent()
        new_hand = []
        for card in self.hand:
            new_hand.append(card.copy())
        new_agent.hand = new_hand
        return new_agent
