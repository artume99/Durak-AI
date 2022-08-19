import copy
import math
from collections import namedtuple
from typing import List

import pygame

from Deck import Deck
from Game import RandomOpponentAgent, Action
from Game import Agent
from Constants import *


class GameState:
    def __init__(self, deck: Deck = None, done=False, attacker=None, defender=None, card_in_play=None,
                 cards_on_board=None):
        super(GameState, self).__init__()
        self.attacker = attacker  # can remove the defender state as it will always be the opposition of the attacker
        self.defender = defender
        self.deck = deck
        self.looser = None
        self._done = done
        self.card_in_play = card_in_play
        self.cards_on_board = cards_on_board if cards_on_board else []

        self.load_image_assets()
        self.back_image = self.deck.back_image.copy()
        self.deck_x, self.deck_y = (SCREEN_WIDTH // 3), (SCREEN_HEIGHT // 2) - (
                self.back_image.get_rect().size[
                    1] // 2)  # todo: why does this line happen 2 times? once here and once in Deck.py?
        self.show_card_size = False

    @property
    def done(self):
        return self._done

    def load_image_assets(self):
        for c in self.deck.cards_list:
            c.load_image_assets()

    def render(self, screen):
        self.draw_deck(screen)
        self.draw_players(screen)
        self.deck.render(screen)

    def draw_players(self, screen):
        players = [self.attacker, self.defender]
        for p in players:
            if type(p) is not RandomOpponentAgent:
                user_cards_x = SCREEN_WIDTH // 4
                user_cards_x_end = SCREEN_WIDTH - SCREEN_WIDTH // 4
                user_cards_gap = (user_cards_x_end - user_cards_x) / (len(p.hand) + 1)
                for i, c in enumerate(p.hand):
                    temp_card = c.front_image
                    temp_card_height = temp_card.get_rect().size[1] * 2
                    if i == p.selected_card_ind:
                        temp_card_height += 15
                    screen.blit(temp_card,
                                (user_cards_x + i * user_cards_gap,
                                 SCREEN_HEIGHT - temp_card_height // 2))

            else:
                # Left user
                user_cards_y = SCREEN_HEIGHT // 4
                user_cards_y_end = SCREEN_HEIGHT - SCREEN_HEIGHT // 4
                user_cards_gap = (user_cards_y_end - user_cards_y) / (len(p.hand) + 1)
                for i, c in enumerate(p.hand):
                    temp_card = c.back_image
                    temp_card = pygame.transform.rotate(temp_card, 90)
                    temp_card_width = 0
                    screen.blit(temp_card, (-((temp_card_width * 2) // 3),
                                            user_cards_y + i * user_cards_gap))

    def draw_deck(self, screen):
        # main (unused) deck
        back_c_image = self.deck.top_card.back_image
        for i in range(math.ceil(len(self.deck) / 4.5)):
            screen.blit(back_c_image,
                        (self.deck_x + i * 2, self.deck_y + i * 2))

        # kozer
        top_card_image = self.deck.top_card.front_image
        screen.blit(top_card_image, (
            self.deck_x - top_card_image.get_rect().size[0], self.deck_y))

        for i in range(len(self.cards_on_board)):
            if i % 2 == 1:
                offset = 25
            else:
                offset = 0
            loc = CARDS_ON_BOARD_LOCS[i // 2]
            screen.blit(self.cards_on_board[i].front_image, (loc[1] + offset, loc[0] + offset))
        return True

    def reshuffle(self):
        self.deck.build()

    def get_legal_actions(self, agent_index):
        if agent_index == 0:
            return self.get_agent_legal_actions()
        elif agent_index == 1:
            return self.get_opponent_legal_actions()
        else:
            raise Exception("illegal agent index.")

    def apply_agent_actions(self, action):
        """
        Checks the type of the player (attack, defend) and returns it's actions
        :return:
        """
        if type(self.attacker) is RandomOpponentAgent:
            return self.apply_defend_action(action)
        else:
            return self.apply_attack_action(action)

    def apply_opponent_action(self, action):
        if type(self.attacker) is RandomOpponentAgent:
            self.apply_attack_action(action)
        else:
            return self.apply_defend_action(action)

    def get_opponent_legal_actions(self):
        """
        Checks the type of the opponent (attack, defend) and returns it's actions
        :return:
        """
        if type(self.attacker) is RandomOpponentAgent:
            return self.attacking_actions()
        else:
            return self.defending_actions()

    def attacking_actions(self):
        if len(self.cards_on_board) == 6 or len(self.attacker.hand) == 0:
            return [Action.BETA]  # Return beta, max 6 cards on board
        actions = []
        if len(self.cards_on_board) > 0:  # Add beta action if there is a card in play
            actions.append(Action.BETA)
        if not self.card_in_play:
            return self.attacker.hand
        for card in self.attacker.hand:
            if self._can_use_attacking_card(card):
                actions.append(card)
        return actions

    def defending_actions(self):
        if len(self.defender.hand) == 0:
            return [Action.BETA]  # Hands is empty
        actions = [Action.TAKE]
        for card in self.defender.hand:
            if self._can_defend_card_in_play(card):
                actions.append(card)
        return actions

    def _can_use_attacking_card(self, card):
        ranks_in_play = []
        for c in self.cards_on_board:
            ranks_in_play.append(c.rank)
        if card.rank in ranks_in_play:
            return True
        return False

    def _can_defend_card_in_play(self, card):
        """
        checks if "card" can attack the card in play
        :param card:
        :return:
        """
        return (card.suit == self.card_in_play.suit and card.rank > self.card_in_play.rank) \
               or (card.is_kozer() and not self.card_in_play.is_kozer())

    def get_agent_legal_actions(self):
        """
        Checks the type of the player (attack, defend) and returns it's actions
        :return:
        """
        if type(self.attacker) is RandomOpponentAgent:
            return self.defending_actions()
        else:
            return self.attacking_actions()

    def apply_attack_action(self, action):
        if action is Action.BETA:
            self._replenish_cards_for_players()
            self._clear_board(True)
            self._switch_roles()
        else:  # Place card
            self.card_in_play = action
            self.place_card(self.attacker, action)
        self._check_looser()

    def apply_defend_action(self, action):
        if action is Action.BETA:
            self._replenish_cards_for_players()
            self._clear_board(True)
            self._switch_roles()
        elif action is Action.TAKE:
            self.defender.extend_hand(self.cards_on_board)
            self._replenish_cards(self.attacker)
            self._clear_board()
        else:  # Place card
            self.place_card(self.defender, action)
        self._check_looser()

    def place_card(self, player, card):
        player.hand.remove(card)
        self.cards_on_board.append(card)

    def _switch_roles(self):
        self.attacker, self.defender = self.defender, self.attacker

    def _clear_board(self, move_to_beta: bool = False):
        if move_to_beta:
            self.deck.add_to_beta(self.cards_on_board)
        self.card_in_play = None
        self.cards_on_board.clear()

    def _check_looser(self):
        """
        Checks if there is a looser, null if there is no looser
        :return:
        """
        if len(self.deck) > 0:
            return
        if len(self.attacker.hand) == 0:
            self.looser = self.defender
            self._done = True
        elif len(self.defender.hand) == 0:
            self.looser = self.attacker
            self._done = True

    def finish_game(self):
        self._done = False
        self.cards_on_board = []
        self.card_in_play = None

    def _replenish_cards_for_players(self):
        """
        check if either player needs more cards and give them if necessary
        the attacker gets cards first
        :return:
        """
        if len(self.deck.cards_list) <= 0:
            return
        self._replenish_cards(self.attacker)
        self._replenish_cards(self.defender)

    def _replenish_cards(self, player: Agent):
        cards_needed = max(0, 6 - len(player.hand))
        player.extend_hand(self.deck.hand_out_cards(cards_needed))

    def generate_successor(self, agent_index, action):
        """
        generates the successor state by apllying action
        :param agent_index:
        :param action:
        :return:
        """
        new_deck = self.deck.copy()
        attacker = self.attacker.copy()
        defender = self.defender.copy()
        # attacker = copy.copy(self.attacker)
        # defender = copy.copy(self.defender)
        successor = GameState(deck=new_deck, done=self._done, attacker=attacker,
                              defender=defender, card_in_play=copy.copy(self.card_in_play),
                              cards_on_board=copy.copy(self.cards_on_board))
        if agent_index == 0:
            successor.apply_agent_actions(action)
        elif agent_index == 1:
            successor.apply_opponent_action(action)
        else:
            raise Exception("illegal agent index.")
        return successor
