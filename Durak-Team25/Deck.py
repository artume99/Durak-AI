import numpy as np
import pygame
# from pygments.styles.paraiso_dark import BLUE

from Constants import *
from Card import Card


ranks = list(range(6, 15))  # not supposed to use 2-5 ranked cards


class Deck:
    """

    """

    def __init__(self, card_list=None, beta_card=None, kozer=None, top_card=None, build=True):
        if beta_card is None:
            beta_card = []
        if card_list is None:
            card_list = []
        self.cards_list, self.beta_cards = card_list, beta_card
        self.kozer = kozer
        self.top_card = top_card
        if build:
            self.build()

        self.attack_list, self.defense_list = [], []
        self.back_image = self.top_card.current_image.copy()  # PROBLEM I THINK
        self.deck_x, self.deck_y = (SCREEN_WIDTH // 3), (SCREEN_HEIGHT // 2) - (
                self.back_image.get_rect().size[
                    1] // 2)  # todo: why does this line happen 2 times? once here and once in GameState.py?
        self.card_pos = {0: []}
        self.found_size = False

    def build(self):
        self.cards_list, self.beta_cards = [], []
        for s in SUITS:
            for r in ranks:
                self.cards_list.append(Card(r, s))
        self.shuffle()
        self.flip_top_card()

    def flip_top_card(self):
        # To be called at the start of the game, before cards are dealt
        self.top_card = self.pop()
        self.top_card.kozer = True
        self.kozer = self.top_card.suit
        for card in self.cards_list:
            if card.suit == self.kozer:
                card.kozer = True
        self.cards_list.insert(0, self.top_card)  # should be the last card of the card list
        # self.opened_cards.insert(0, self.top_card)

    def shuffle(self):
        np.random.shuffle(self.cards_list)

    def pop(self):
        return self.cards_list.pop()

    def __len__(self):
        return len(self.cards_list)

    def __str__(self):
        return "Deck has {} cards left".format(len(self.cards_list))

    def hand_out_cards(self, num):
        """
        give a maximum of num cards
        :param num:
        :return:
        """
        cards_to_hand = []
        num_of_card_to_hand = min(num, len(self.cards_list))
        for i in range(num_of_card_to_hand):
            cards_to_hand.append(self.pop())
        return cards_to_hand

    def add_to_beta(self, cards):
        self.beta_cards.extend(cards)

    def get_card_indexes(self, card_count_x, card_count_y):
        card_width, card_height = self.back_image.get_rect().size
        card_gap = 110

        left_row_x = (self.deck_x - card_width) - (
                (SCREEN_WIDTH - card_width // 2) - (
                self.deck_y + card_width) - card_width) // 2
        for c_index in range(1, card_count_y + 1):
            # (c_index through cardD_count_y // 2)
            cx_index = c_index % (card_count_y // 2) if c_index % (
                    card_count_y // 2) != 0 else card_count_y // 2
            cy_index = (c_index - cx_index) // (card_count_y // 2)
            if cx_index == 1:
                left_row_y = SCREEN_HEIGHT // 2 - card_width // 2
                temp_pos = (left_row_x * (cy_index + 1), left_row_y, 90)
                position_list = self.card_pos.get(c_index - 1).copy()
                position_list.append(temp_pos)
                self.card_pos.update({c_index: position_list})
            elif cx_index % 2 == 0:
                left_row_y = SCREEN_HEIGHT // 2 - card_width - card_gap // 4
                position_list = self.card_pos.get(c_index - 2).copy()
                for i in range(len(position_list), c_index):
                    if i == 0:
                        temp_y = left_row_y
                    elif i % 2 == 0:
                        temp_y = left_row_y - ((card_width + card_gap // 2) * (
                                i - i // 2))
                    else:
                        temp_y = left_row_y + ((card_width + card_gap // 2) * (
                                i - i // 2))
                    temp_pos = (left_row_x * (cy_index + 1), temp_y, 90)
                    position_list.append(temp_pos)
                self.card_pos.update({c_index: position_list})
            elif cx_index % 2 == 1:
                left_row_y = SCREEN_HEIGHT // 2 - card_width // 2
                position_list = self.card_pos.get(c_index - 2).copy()
                for i in range(len(position_list), c_index):
                    if i == 0:
                        temp_y = left_row_y
                    elif i % 2 == 0:
                        temp_y = left_row_y - ((card_width + card_gap // 2) * (
                                i - i // 2))
                    else:
                        temp_y = left_row_y + ((card_width + card_gap // 2) * (
                                i - i // 2))
                    temp_pos = (left_row_x * (cy_index + 1), temp_y, 90)
                    position_list.append(temp_pos)
                self.card_pos.update({c_index: position_list})

    def render(self, screen):
        # GOAL->Draw for each space for each row given the size
        card_width, card_height = self.back_image.get_rect().size
        card_gap = 110

        # GET THE WIDTH POSSIBLE
        # bottom row must be below (self.deck_y + card_height)
        build_size_width, build_size_height = card_width, card_width
        card_count_x = 1
        card_count_y = 1
        while not self.found_size:
            found_x_card_count = build_size_width + card_gap + card_width >= SCREEN_WIDTH - (
                    2 * card_height // 3)
            found_y_card_count = build_size_width + card_gap + card_width >= SCREEN_HEIGHT - (
                    5 * card_height // 6)
            if found_x_card_count and found_y_card_count:
                self.found_size = True
                self.get_card_indexes(card_count_x, card_count_y * 2)
            if not found_x_card_count:
                build_size_width = build_size_width + card_gap // 2 + card_width
                card_count_x += 1
            if not found_y_card_count:
                build_size_height = build_size_height + card_gap // 2 + card_width
                card_count_y += 1
        attack_card_points = self.card_pos[len(self.attack_list)]

        # Positions to draw
        for i, c in enumerate(self.attack_list):
            temp_screen = pygame.transform.rotate(c.front_image,
                                                  attack_card_points[i][2])
            screen.blit(temp_screen,
                        (attack_card_points[i][0], attack_card_points[i][1]))

        for i, c in enumerate(self.defense_list):
            temp_screen = pygame.transform.rotate(c.front_image,
                                                  attack_card_points[i][2])
            screen.blit(c.front_image, (attack_card_points[i][0] + 13, attack_card_points[i][1] + 13))

        font = pygame.font.SysFont(None, 24)
        img = font.render(str(self), True, BLUE)
        screen.blit(img, (20, 20))

        # temp_rect = pygame.rect.Rect()
        # draw all played cards in the correct place lol

    def copy(self):
        new_card_list = []
        new_beta_list = []
        for card in self.cards_list:
            new_card_list.append(card.copy())
        new_deck = Deck(card_list=new_card_list, beta_card=new_beta_list, kozer=self.kozer,
                        top_card=self.top_card.copy(), build=False)
        return new_deck
