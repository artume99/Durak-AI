from itertools import product
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
WIDTH_1_2 = SCREEN_WIDTH / 2
HEIGHT_1_10 = SCREEN_HEIGHT / 10
GREEN = (7, 99, 36)
BLUE = (0, 0, 255)
HIGH_CARDS = {11, 12, 13, 14}
LOW_CARDS = {6, 7, 8}
SUITS = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
MSG_FOR_KEYBOARD_AGENT = "\ntake: down, place_card: space, swipe_right: right, swipe_left: left beta: up\n"
# CARDS_ON_BOARD_LOCS = list(product([80, 280], [650, 850, 1050]))
CARDS_ON_BOARD_LOCS = list(product([HEIGHT_1_10, HEIGHT_1_10 + 200], [WIDTH_1_2, WIDTH_1_2 + 170, WIDTH_1_2 + 340]))
WINS_LAST_ITER = "wins.pk"
WEIGHT_VECTOR = "weight_vector.pk"
