import pygame

class Card():
    def __init__(self, rank, suit):
        super(Card, self).__init__()
        self.load_image_assets()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.regular_card_factor = 0.8

        self.rank = rank
        self.suit = suit
        self.kozer = False

    def load_image_assets(self):
        self.back_image = pygame.image.load('Res/Cards/BackCard.png').convert_alpha()
        self.front_image = pygame.image.load("Res/Cards/{}{}.png".format(self.suit, str(self.rank))).convert_alpha()
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
