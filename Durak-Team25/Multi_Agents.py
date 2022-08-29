import copy
import math
import os.path
import pickle
import sys
from enum import Enum
from typing import Tuple, List

import numpy as np

from Card import Card
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
                    action = card
                elif event.key == K_DOWN:
                    action = Action.TAKE
                elif event.key == K_UP:
                    action = Action.BETA
                elif event.key == K_RIGHT:
                    self.selected_card_ind += 1
                    if self.selected_card_ind >= len(self.hand):
                        self.selected_card_ind = 0
                        # state.draw_players(state.screen)
                    print("currently selected card: ", end="")
                    print(self.hand[self.selected_card_ind])
                    print(MSG_FOR_KEYBOARD_AGENT)
                    action = Action.SWIPE
                elif event.key == K_LEFT:
                    self.selected_card_ind -= 1
                    if self.selected_card_ind < 0:
                        self.selected_card_ind = len(self.hand) - 1
                        print("currently selected card: ", end="")
                        print(self.hand[self.selected_card_ind])
                        print(MSG_FOR_KEYBOARD_AGENT)
                    action = Action.SWIPE
                else:
                    continue
                if action not in state.get_legal_actions(0) + [Action.SWIPE]:
                    print(f"Action {action} is Illegal ", file=sys.stderr)
                    continue
                if action is not Action.SWIPE:
                    self.selected_card_ind = 0
                return action
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def stop_running(self):
        self._should_stop = True

    def copy(self):
        new_agent = KeyboardAgent()
        new_hand = []
        for card in self.hand:
            new_hand.append(card.copy())
        new_agent.hand = new_hand
        return new_agent


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


def get_hand_dicts(hand: List[Card]):
    card_ranks = Counter()
    card_suits = [0 for i in range(4)]
    for card in hand:
        card_ranks[card.rank] += 1
        card_suits[suits[card.suit]] += 1
    return card_ranks, np.array(card_suits)


def rank_on_board(game_state: GameState, card_rank: int):
    """
    Calculates how many cards of a certain rank there are currently on the board
    :param game_state: The current game state
    :param card_rank: The desired rank
    :return: int
    """
    cards_amount = 0
    for card in game_state.cards_on_board:
        if card.rank == card_rank:
            cards_amount += 1
    return cards_amount


def rank_in_hand(hand: List[Card], card_rank: int):
    """
    Calculates how many cards of a certain rank there are currently in hand
    :param hand: Holding hand
    :param card_rank: The desired rank
    :return: int
    """
    cards_amount = 0
    for card in hand:
        if card.rank == card_rank:
            cards_amount += 1
    return cards_amount


def high_triplets_board(game_state: GameState):
    """
    Is there a triplet of high card on the board?
    :param game_state: The current game state
    :return: True if there is at least one triplet of high cards, False o.w.
    """
    for rank in HIGH_CARDS:
        if rank_on_board(game_state, rank) >= 3:
            return True
    return False


def high_triplets_hand(hand: List[Card]):
    """
    Is there a triplet of high card in hand?
    :param hand: Holding hand
    :return: True if there is at least one triplet of high cards, False o.w.
    """
    for rank in HIGH_CARDS:
        if rank_in_hand(hand, rank) >= 3:
            return True
    return False


def individual_highs_on_board(game_state: GameState, attacker: bool):
    """
    Calculates how many "high" ranked cards a certain player (the defender or the attacker) has put on the board
    :param game_state: The current game state
    :param attacker: Do we search for the attacker's highs, or the defender's highs?
    :return: int
    """
    highs = 0
    for i in range(len(game_state.cards_on_board)):
        if attacker and i % 2 == 0 and game_state.cards_on_board[i].rank in HIGH_CARDS:
            highs += 1
        elif not attacker and i % 2 == 1 and game_state.cards_on_board[i].rank in HIGH_CARDS:
            highs += 1
    return highs


def highs_percentage(game_state: GameState):
    """
    Calculates the percentage of the "high" ranked cards among all of the cards currently on board
    :param game_state: The current game state
    :return: float
    """
    highs_amount = 0
    highs_amount += individual_highs_on_board(game_state, True)
    highs_amount += individual_highs_on_board(game_state, False)
    return highs_amount / len(game_state.cards_on_board)


def individual_lows_on_board(game_state: GameState, attacker: bool):
    lows = 0
    for i in range(len(game_state.cards_on_board)):
        if attacker and i % 2 == 0 and game_state.cards_on_board[i].rank in LOW_CARDS:
            lows += 1
        elif not attacker and i % 2 == 1 and game_state.cards_on_board[i].rank in LOW_CARDS:
            lows += 1
    return lows


def highs_in_hand(hand: List[Card]):
    highs = 0
    for card in hand:
        if card.rank in HIGH_CARDS:
            highs += 1
    return highs


def individual_kozers_on_board(game_state: GameState, attacker: bool):
    """
    Calculates how many kozers a certain player (the defender or the attacker) has put on the board
    :param game_state: The current game state
    :param attacker: Do we search for the attacker's kozers, or the defender's kozers?
    :return: int
    """
    kozers = 0
    for i in range(len(game_state.cards_on_board)):
        if attacker and i % 2 == 0 and game_state.cards_on_board[i].is_kozer():
            kozers += 1
        elif not attacker and i % 2 == 1 and game_state.cards_on_board[i].is_kozer():
            kozers += 1
    return kozers


def kozer_percentage(game_state: GameState):
    """
    Calculates the percentage of the kozers among all of the cards currently on board
    :param game_state: The current game state
    :return: float
    """
    kozer_amount = 0
    kozer_amount += individual_kozers_on_board(game_state, True)
    kozer_amount += individual_kozers_on_board(game_state, False)
    return kozer_amount / len(game_state.cards_on_board) if len(game_state.cards_on_board) else 0


def is_legal_defend(attacking_card: Card, defending_card: Card):
    """
    Checks whether we can defend an attack of op_card with a given card
    :param attacking_card: Attacking card
    :param defending_card: Defending card
    :return: True if we can defend against the attacking card, False o.w.
    """
    if attacking_card.is_kozer() and not defending_card.is_kozer():
        return False
    if not attacking_card.is_kozer() and defending_card.is_kozer():
        return True
    if attacking_card.rank < defending_card.rank:
        return True
    return False


def can_defend(op_card: Card, hand: List[Card]):
    """
    Checks whether we can defend an attack of op_card with any of the cards in our hand
    :param op_card: Attacking card
    :param hand: Our hand
    :return: True if there is a card that we can defend with, False o.w.
    """
    for card in hand:
        if is_legal_defend(op_card, card):
            return True
    return False


def num_of_variety(game_state: GameState):
    variety = set()
    for card in game_state.cards_on_board:
        variety.add(card.rank)
    return len(variety)


def weaknesses_count(game_state: GameState, hand: List[Card], op_hand: List[Card]):
    """
    Calculates the weak spots we have against the op, meaning: cards that we can't defend ourselves against
    :param game_state: The current game state
    :param hand: Our hand
    :param op_hand: The op's hand
    :return: int
    """
    known_op_hand = game_state.known_cards.intersection(op_hand)
    weaknesses = len(op_hand) - len(known_op_hand)  # first of all, the diff between the cards there are in the op's
    # hand and the cards that we know of is already a weakness
    for card in known_op_hand:
        if not can_defend(card, hand):
            weaknesses += 1
    return weaknesses


def strong_suit(game_state: GameState, suit, hand: List[Card],
                op_hand: List[Card]):  # todo: figure out where should i use it
    """
    Checks whether a certain suit is considered "strong", meaning that we have it but our op doesn't
    :param game_state: The current game state
    :param suit: The desired suit
    :param hand: Our hand
    :param op_hand: The op's hand
    :return: True if the suit is strong in our hands, False o.w.
    """
    is_suit = False
    is_op_suit = False
    known_op_hand = game_state.known_cards.intersection(op_hand)
    for card in hand:
        if card.suit == suit:
            is_suit = True
    for card in known_op_hand:
        if card.suit == suit:
            is_op_suit = True
    return True if (is_suit and not is_op_suit) else False


def strong_suit_evaluation(game_state: GameState, hand: List[Card],
                           op_hand: List[Card]):  # todo: figure out where should i use it
    """
    Calculates the amount of strong suits we hold in our hand. Kozer-suit gets more recognition
    :param game_state: The current game state
    :param hand: Our hand
    :param op_hand: The op's hand
    :return: int
    """
    strong_suits = 0
    for suit in SUITS:
        if strong_suit(game_state, suit, hand, op_hand):
            if game_state.is_suit_kozer(suit):
                strong_suits += 4  # a kozer-strong-suit gets more recognition
            else:
                strong_suits += 1
    return strong_suits


def generate_hand_features(game_state: GameState, hand: List[Card], op_hand: List[Card], features: Counter):
    """
    Generates general features that are connected to our hand
    :param game_state: The current game state
    :param hand: Our hand
    :param op_hand: The op's hand
    :param features: A features dict
    """
    deck_amount = max(len(game_state.deck), 1)
    cards_amount = max(len(hand), 1)
    card_ranks, card_suits = get_hand_dicts(hand)
    min_card = None if len(hand) == 0 else min(hand)
    features["kozer amount"] = card_suits[suits[game_state.deck.kozer]]
    features["highs amount"] = highs_in_hand(hand)
    features["num of cards"] = -len(hand)
    features["difference between hands"] = len(op_hand) - len(hand)
    features["mean rank"] = card_ranks.multiply_key_value() / cards_amount
    features["variance suit"] = card_suits.var()
    if min_card:
        features["min card"] = min_card.rank + 6 if min_card.is_kozer() else min_card.rank
    features["high triplets in hand"] = 1 if high_triplets_hand(hand) else 0
    if len(game_state.deck) < 6:
        features["cards on hand"] = -cards_amount / (36 * (len(game_state.deck) + 1))
        features["last turn"] = 1 if len(hand) == 0 else 0


def generate_attack_features(game_state: GameState, features: Counter):
    """
    Generates attacking features
    :param game_state: The current game state
    :param features: A features dict
    """
    deck_amount = max(len(game_state.deck), 1)
    # features["kozers percentage"] = -kozer_percentage(game_state)
    features["lows on board"] = -individual_lows_on_board(game_state, True)  # we prefer NOT to attack with
    # lows as the game proceeds
    features["defender's kozers"] = individual_kozers_on_board(game_state, False)  # as the attacker, it is good for me
    # if the enemy gets rid of kozers
    features["attacker's kozers"] = -individual_kozers_on_board(game_state, True)
    # features["highs percentage"] = -highs_percentage(game_state)
    features["defender's highs"] = individual_highs_on_board(game_state, False)
    features["attacker's highs"] = -individual_highs_on_board(game_state, True)
    features["high triplets on board"] = -1 if high_triplets_board(
        game_state) else 1  # letting the defender hold onto a
    # triplet is far worse than bita


def generate_defend_features(game_state: GameState, hand: List[Card], op_hand: List[Card], features: Counter):
    """
    Generates defending features
    :param game_state: The current game state
    :param hand: Our hand
    :param op_hand: The op's hand
    :param features: A features dict
    """
    cards_on_board = len(game_state.cards_on_board)
    # todo: add a feature that takes in count the amount of high triplets: on board + in hand (keep it with low weight)
    features["variance rank on board"] = 0 if not game_state.cards_on_board else -num_of_variety(game_state)
    features["vulnerability"] = -weaknesses_count(game_state, hand, op_hand)
    features["num of attacks rate"] = -math.pow(cards_on_board - 4, 2)  # 2 attacks are good for us, we get rid of
    # cards, but the more attacks there are - the bigger the chance we take everything


def generate_op_hand_features(game_state: GameState, hand: List[Card], op_hand: List[Card],
                              features: Counter):  # todo: see if needed
    """
    gives features for evaluating our op hand (using the cards we ASSUME he holds)
    :param game_state:
    :param hand:
    :param op_hand:
    :param features:
    :return:
    """
    known_op_hand = game_state.known_cards.intersection(op_hand)


def calculate_random_weights(weights: Counter):
    calculate_weights(weights)
    for key, value in weights.items():
        weights[key] = np.random.randint(0, 100)  # maybe random.uniform is better


def calculate_weights(weights, mult=1):
    # hand features
    weights["kozer amount"] = 50 * mult
    weights["highs amount"] = 10 * mult
    weights["num of cards"] = 20 * mult
    weights["difference between hands"] = 15 * mult
    weights["mean rank"] = 12 * mult
    weights["variance suit"] = 7 * mult
    weights["min card"] = 90 * mult
    weights["high triplets in hand"] = 20 * mult
    weights["cards on hand"] = 45 * mult
    weights["last turn"] = 10000 * mult  # "inf" is not good! it evaluates the actions as "nan" and gives "STOP" action!

    # attacker features
    weights["lows on board"] = 10 * mult
    weights["defender's kozers"] = 45 * mult
    weights["attacker's kozers"] = 55 * mult
    weights["defender's highs"] = 50 * mult
    weights["attacker's highs"] = 10 * mult
    weights["high triplets on board"] = 10 * mult

    # defender features
    weights["variance rank on board"] = 30 * mult
    weights["vulnerability"] = 72 * mult
    weights["num of attacks rate"] = 41 * mult


def base_evaluation(game_state: GameState):
    pygame.event.pump()
    features = Counter()
    if game_state.is_attacking(Player):
        hand, op_hand = game_state.attacker.hand, game_state.defender.hand
        generate_attack_features(game_state, features)
    else:
        op_hand, hand = game_state.attacker.hand, game_state.defender.hand
        generate_defend_features(game_state, hand, op_hand, features)
    generate_hand_features(game_state, hand, op_hand, features)
    # features.normalize()

    weights = Counter()
    calculate_weights(weights)

    score = 0
    final = {}
    for feature in features.keys():
        score += (weights[feature] * features[feature])
        final[feature] = (weights[feature] * features[feature])
    Actions[game_state.last_action] = score, final
    return score


Actions = Counter()


def genetic_evaluation(game_state: GameState, weights: Counter):
    pygame.event.pump()
    features = Counter()
    if game_state.is_attacking(0):
        hand, op_hand = game_state.attacker.hand, game_state.defender.hand
        generate_attack_features(game_state, features)
    else:
        op_hand, hand = game_state.attacker.hand, game_state.defender.hand
        generate_defend_features(game_state, hand, op_hand, features)
    generate_hand_features(game_state, hand, op_hand, features)
    # features.normalize()

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
        expectimax = self.expctimax(game_state, self.depth, Player)
        return expectimax[1]

    def expctimax(self, game_state: GameState, depth: int, agent: int):
        # region End Condition
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region Expected Max
        if agent == Player:
            legal_moves = game_state.get_legal_actions(agent)
            max_val = (float("-inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent, move)
                response_val = self.expctimax(new_state, depth - 1, Computer)[0], move
                max_val = max(max_val, response_val, key=costume_key)
            return max_val

        # endregion

        # region Expected Min
        if agent == Computer:
            legal_moves = game_state.get_legal_actions(agent)
            succesors = []
            for move in legal_moves:
                succesors.append(game_state.generate_successor(agent, move))
            succesors = np.array(succesors)
            probability_s = 1 / len(succesors)
            vfunc_expectimax = np.vectorize(self.expctimax)
            responses = vfunc_expectimax(succesors, depth, Player)
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
        minimax = self.minimax(game_state, self.depth, Player)
        return minimax[1]

    def minimax(self, game_state: GameState, depth: int, agent: int) -> Tuple[int, Action]:
        # region if 𝑑𝑒𝑝𝑡ℎ = 0 or v is a terminal node then return 𝑢(𝑣)
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region  if isMaxNode then return max
        if agent == Player:
            legal_moves = game_state.get_legal_actions(agent)
            max_val = (float("-inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent, move)
                response_val = self.minimax(new_state, depth - 1, Computer)[0], move
                max_val = max(max_val, response_val, key=costume_key)
            return max_val

        # endregion

        # region  if isMinNode then return min
        if agent == Computer:
            legal_moves = game_state.get_legal_actions(agent)
            min_val = (float("inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent, move)
                response_val = self.minimax(new_state, depth, Player)[0], move
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


class GeneticAgent(MinmaxAgent):
    def __init__(self, weight):
        super().__init__()
        self.evaluation_function = genetic_evaluation
        self.depth = 1
        self.weight_vector = weight

    def minimax(self, game_state: GameState, depth: int,
                agent: int) -> Tuple[int, Action]:
        # region if 𝑑𝑒𝑝𝑡ℎ = 0 or v is a terminal node then return 𝑢(𝑣)
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state, self.weight_vector), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region  if isMaxNode then return max
        if agent == Player:
            legal_moves = game_state.get_legal_actions(agent)
            max_val = (float("-inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent, move)
                response_val = self.minimax(new_state, depth - 1, Computer)[0], move
                max_val = max(max_val, response_val, key=costume_key)
            return max_val

        # endregion

        # region  if isMinNode then return min
        if agent == Computer:
            legal_moves = game_state.get_legal_actions(agent)
            min_val = (float("inf"), Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent,
                                                          move)
                response_val = \
                    self.minimax(new_state, depth, Player)[0], move
                min_val = min(min_val, response_val, key=costume_key)
            return min_val
        # endregion

    def copy(self):
        new_agent = GeneticAgent(weight=None)
        new_hand = []
        for card in self.hand:
            new_hand.append(card.copy())
        new_agent.hand = new_hand
        return new_agent


class AlphaBetaAgent(MultiAgentSearchAgent):

    def get_action(self, game_state: GameState):

        alpha_beta = self.alpha_beta(game_state, Player, self.depth)
        return alpha_beta[1]

    def alpha_beta(self, game_state: GameState, agent: int, depth: int, alpha=float("-inf"), beta=float("inf")) -> \
            Tuple[int, Action]:
        # region End Condition
        if depth == 0 or game_state.done:
            return self.evaluation_function(game_state), Action.STOP
        # endregion

        costume_key = lambda x: x[0]

        # region alpha pruning
        if agent == Player:
            legal_moves = game_state.get_legal_actions(agent)
            return_alpha = (alpha, Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent, move)
                alpha = return_alpha[0]
                response_val = self.alpha_beta(new_state, Computer, depth - 1, alpha, beta)[0], move
                return_alpha = max(return_alpha, response_val, key=costume_key)
                if return_alpha[0] >= beta:
                    break
            return return_alpha
        # endregion

        # region beta pruning
        if agent == Computer:
            legal_moves = game_state.get_legal_actions(agent)
            return_beta = (beta, Action.STOP)
            for move in legal_moves:
                new_state = game_state.generate_successor(agent, move)
                beta = return_beta[0]
                response_val = self.alpha_beta(new_state, Player, depth, alpha, beta)[0], move
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
