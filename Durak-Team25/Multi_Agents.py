import copy
import os.path
import pickle
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

    def stop_running(self):
        self._should_stop = True


suits = {
    'Spades': 0,
    'Hearts': 1,
    'Diamonds': 2,
    'Clubs': 3,
    0: 'Spades',
    1: 'Hearts',
    2: 'Diamonds',
    3: 'Clubs'

}


def get_hand_dicts(hand):
    card_ranks = Counter()
    card_suits = [0 for i in range(4)]
    for card in hand:
        card_ranks[card.rank] += 1
        card_suits[suits[card.suit]] += 1
    return card_ranks, np.array(card_suits)


def rank_on_board(game_state, card_rank: int):
    cards_amount = 0
    for card in game_state.cards_on_board:
        if card.rank == card_rank:
            cards_amount += 1
    return cards_amount


def high_threesomes(game_state):
    """
    Is there a threesome of high card on the board?
    :param game_state: The current game state
    :return: True if there is at least one threesome of high cards, False otherwise
    """
    for rank in HIGH_CARDS:
        if rank_on_board(game_state, rank) >= 3:
            return True
    return False


def highs_percentage(game_state):
    highs_amount = 0
    for card in game_state.cards_on_board:
        if card.rank in HIGH_CARDS:
            highs_amount += 1
    return highs_amount / len(game_state.cards_on_board)


def kozers_on_board(game_state, attacker: bool):
    on_board_amount = len(game_state.cards_on_board)
    kozer_amount = 0
    if attacker:
        for i in range((on_board_amount // 2) + 1):
            if game_state.cards_on_board[i * 2].is_kozer():
                kozer_amount += 1
    else:
        for i in range(on_board_amount // 2):
            if game_state.cards_on_board[i * 2 + 1].is_kozer():
                kozer_amount += 1
    return kozer_amount


def kozer_percentage(game_state): #todo: check where this function should be, maybe some kind of utils?
    kozer_amount = 0
    for card in game_state.cards_on_board:
        if card.is_kozer():
            kozer_amount += 1
    return kozer_amount / len(game_state.cards_on_board)


def highs_on_board(game_state, attacker: bool):
    on_board_amount = len(game_state.cards_on_board)
    highs_amount = 0
    if attacker:
        for i in range((on_board_amount // 2) + 1):
            if game_state.cards_on_board[i * 2].rank in HIGH_CARDS:
                highs_amount += 1
    else:
        for i in range(on_board_amount // 2):
            if game_state.cards_on_board[i * 2 + 1].rank in HIGH_CARDS:
                highs_amount += 1
    return highs_amount


def generate_attack_features(game_state, features):
    features["kozers_percentage"] = -kozer_percentage(game_state)
    features["defender's_kozers"] = kozers_on_board(game_state, False) #as the attacker, it is good for me if the enemy
    # gets rid of kozers
    features["attacker's_kozers"] = -kozers_on_board(game_state, True)
    features["highs_percentage"] = -highs_percentage(game_state)
    features["defender's_highs"] = highs_on_board(game_state, False)
    features["attacker's_highs"] = -highs_on_board(game_state, True)
    features["high_threesomes"] = -1 if high_threesomes(game_state) else 1 #letting the defender hold onto a threesome
    # is far worse than bita
    # features[""]


def generate_defend_features(game_state, features):
    features["kozers_percentage"] = -kozer_percentage(game_state) #1: i'm still not sure if it's good or bad for the
    # defender, probably useless.. 2: on second thought, it's better for me as the defender not to have kozers on the board
    features["defender's_kozers"] = -kozers_on_board(game_state, False) #as the defender, i don't want to get rid of
    # kozers MORE THAN I HAVE TO. need to think about it, it depends on the kozer and on the amount of cards on board..
    features["attacker's_kozers"] = kozers_on_board(game_state, True) #is it good though? I'm afraid it will prompt a
    # move that will make the attacker attack me with more kozers.. it's nice when the enemy gets rid of kozers, but
    # it's better when he doesn't attck me with them


def generate_hand_features(game_state, hand, op_hand, features):
    deck_amount = max(len(game_state.deck), 1)
    cards_amount = max(len(hand), 1)
    card_ranks, card_suits = get_hand_dicts(hand)
    features["kozer amount"] = card_suits[suits[game_state.deck.kozer]]
    features["num of cards"] = -len(hand) / deck_amount
    features["difference between hands"] = (len(op_hand) - len(hand)) / deck_amount
    features["mean_rank"] = card_ranks.multiply_key_value() / cards_amount
    features["variance_rank"] = sum((features["mean_rank"] - card.rank) ** 2 for card in hand) / cards_amount
    features["variance_suit"] = card_suits.var()
    features["min_card"] = 15 if len(hand) == 0 else hand[-1].rank
    features["max_card"] = 15 if len(hand) == 0 else hand[0].rank
    features["hand_sum"] = 0 if len(hand) == 0 else sum([card.rank for card in hand])
    if len(game_state.deck) < 6:
        features["cards_on_hand"] = -cards_amount / (36 * (len(game_state.deck) + 1))


def calculate_weights(weights):
    # hand features
    # weights["kozer amount"] = 12
    # weights["num of cards"] = 20
    weights["difference between hands"] = 1 #15
    # weights["mean_rank"] = 3
    # # weights["variance_rank"] = 2
    # weights["variance_suit"] = 7
    # weights["min_card"] = 10
    # weights["max_card"] = 3
    # weights["cards_on_hand"] = 45
    # # weights["hand_sum"] = 1

    # attacker features
    # weights["kozers_percentage"] = 0 #useless?
    weights["defender's_kozers"] = 1 #3 priority
    weights["attacker's_kozers"] = 3 #2 priority
    weights["highs_percentage"] = 1 #1 priority
    weights["defender's_highs"] = 3
    weights["attacker's_highs"] = 1 #1 priority
    weights["high_threesomes"] = 1

    # defender features


def base_evaluation(game_state):
    features = Counter()
    if game_state.is_attacking(0):
        hand, op_hand = game_state.attacker.hand, game_state.defender.hand
        generate_attack_features(game_state,features)
    else:
        op_hand, hand = game_state.attacker.hand, game_state.defender.hand
        # generate_defend_features()
    generate_hand_features(game_state,hand, op_hand, features)
    # features.normalize()

    weights = Counter()
    calculate_weights(weights)

    score = 0
    final = {}
    for feature in features.keys():
        score += (weights[feature] * features[feature])
        final[feature] = (weights[feature] * features[feature])

    return score


class GeneticAgent(Agent):
    def __init__(self):
        super().__init__()

        # initialize weight vector
        if not os.path.exists(WEIGHT_VECTOR):
            weights = Counter()
            calculate_weights(weights)
            with open(WEIGHT_VECTOR, 'wb') as f:
                pickle.dump(weights, f)

        # get current weight vector
        with open(WEIGHT_VECTOR, 'rb') as f:
            self.vector = pickle.load(f)
        with open(WINS_LAST_ITER, 'rb') as f:
            self.last_game_wins = pickle.load(f)

    def get_action(self, game_state):
        features = Counter()
        if game_state.is_attacking(0):
            hand, op_hand = game_state.attacker.hand, game_state.defender.hand
            generate_attack_features(game_state, features)
        else:
            op_hand, hand = game_state.attacker.hand, game_state.defender.hand
            # generate_defend_features()
        generate_hand_features(game_state, hand, op_hand, features)
        # features.normalize()

        weights = Counter() * self.vector
        # calculate_weights(weights)


        score = 0
        final = {}
        for feature in features.keys():
            score += (weights[feature] * features[feature])
            final[feature] = (weights[feature] * features[feature])

        return score

class MultiAgentSearchAgent(Agent):
    def __init__(self, evaluation_function=base_evaluation, depth=1):
        super().__init__()
        self.evaluation_function = evaluation_function
        self.depth = depth

    def get_action(self, game_state: GameState):
        return


class ExpectimaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state: GameState):
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


class AlphaBetaAgent(MultiAgentSearchAgent):

    def get_action(self, game_state: GameState):

        alpha_beta = self.alpha_beta(game_state, AgentNum.Player, self.depth)
        return alpha_beta[1]

    def alpha_beta(self, game_state: GameState, agent: AgentNum, depth: int, alpha=float("-inf"), beta=float("inf")) -> \
            Tuple[int, Action]:
        # region End Condition
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region alpha pruning
        if agent == AgentNum.Player:
            legal_moves = game_state.get_legal_actions(agent.value)
            return_alpha = (alpha, Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent.value, move)
                alpha = return_alpha[0]
                response_val = self.alpha_beta(new_state, AgentNum.Computer, depth - 1, alpha, beta)[0], move
                return_alpha = max(return_alpha, response_val, key=costume_key)
                if return_alpha[0] >= beta:
                    break
            return return_alpha
        # endregion

        # region beta pruning
        if agent == AgentNum.Computer:
            legal_moves = game_state.get_legal_actions(agent.value)
            return_beta = (beta, Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent.value, move)
                beta = return_beta[0]
                response_val = self.alpha_beta(new_state, AgentNum.Player, depth, alpha, beta)[0], move
                return_beta = min(return_beta, response_val, key=costume_key)
                if alpha >= return_beta[0]:
                    break
            return return_beta
        # endregion

    def copy(self):
        new_agent = AlphaBetaAgent()
        new_hand = []
        for card in self.hand:
            new_hand.append(card.copy())
        new_agent.hand = new_hand
        return new_agent
