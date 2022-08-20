import pygame
from pygame.locals import RLEACCEL


class Card(pygame.sprite.Sprite):
    def __init__(self, rank, suit, load=True):
        self.rank = rank
        self.suit = suit
        self.kozer = False

        self.regular_card_factor = 0.8
        super(Card, self).__init__()
        # self.surf = pygame.Surface((75, 25))
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.rect = self.surf.get_rect()
        if load:
            self.load_image_assets()

    def load_image_assets(self):
        self.back_image = pygame.image.load('Cards/BackCard.png').convert_alpha()
        self.front_image = pygame.image.load("Cards/{}{}.png".format(self.suit, str(self.rank))).convert_alpha()
        new_width = int(self.back_image.get_rect().size[0] * self.regular_card_factor)
        new_height = int(self.back_image.get_rect().size[1] * self.regular_card_factor)
        self.back_image = pygame.transform.smoothscale(self.back_image, (new_width, new_height))
        self.front_image = pygame.transform.smoothscale(self.front_image, (new_width, new_height))
        self.current_image = self.back_image

    def is_kozer(self):
        return self.kozer

    def __str__(self):
        return str(self.rank) + "" + str(self.suit)

    def __repr__(self):
        return str(self.rank) + "" + str(self.suit)

    def __gt__(self, other):
        if self.is_kozer() and not other.is_kozer():
            return False
        elif not self.is_kozer() and other.is_kozer():
            return True
        t1 = self.rank, self.suit
        t2 = other.rank, other.suit
        return t1 < t2

    def __lt__(self, other):
        if self.is_kozer() and not other.is_kozer():
            return True
        elif not self.is_kozer() and other.is_kozer():
            return False
        t1 = self.rank, self.suit
        t2 = other.rank, other.suit
        return t1 > t2

    def __eq__(self, other):
        if type(other) is Card:
            return self.suit == other.suit and self.rank == other.rank
        return super.__eq__(Card, other)

    def copy(self):
        new_card = Card(self.rank, self.suit, load=False)
        new_card.kozer = self.kozer
        new_card.back_image = self.back_image.copy()
        new_card.front_image = self.front_image.copy()
        new_card.current_image = self.current_image.copy()
        return new_card
