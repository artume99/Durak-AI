import argparse

import numpy
import pygame
from Multi_Agents import *
from Deck import Deck
from Game import Game, RandomOpponentAgent
from GameState import GameState
from Constants import *


class GameRunner(object):
    def __init__(self, agent, sleep_between_actions):
        # Initialize pygame
        pygame.init()
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.sleep_between_actions = sleep_between_actions

        super(GameRunner, self).__init__()
        self._agent = agent
        self.current_game = None

    def new_game(self, initial_state, *args, **kw):
        self.quit_game()
        initial_state.finish_game()
        initial_state.reshuffle()
        op_hand = initial_state.deck.hand_out_cards(6)
        opponent_agent = RandomOpponentAgent(op_hand)
        ag_hand = initial_state.deck.hand_out_cards(6)
        self._agent.hand = ag_hand
        game = Game(self._agent, opponent_agent, sleep_between_actions=self.sleep_between_actions)
        self.current_game = game
        return game.run(initial_state, self.screen)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


def create_agent(args):
    if args.agent == "ExpectimaxAgent":
        agent = ExpectimaxAgent()
    elif args.agent == "KeyboardAgent":
        agent = KeyboardAgent()
    elif args.agent == "MinimaxAgent":
        agent = MinmaxAgent()
    return agent


def main():
    parser = argparse.ArgumentParser(description='Durak game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100),
                        type=int)
    # displays = ['GUI', 'SummaryDisplay']
    agents = ["KeyboardAgent", 'ExpectimaxAgent', "MinimaxAgent"]
    # parser.add_argument('--display', choices=displays, help='The game ui.', default=displays[0], type=str)
    parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[2], type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=3, type=int)

    parser.add_argument('--evaluation_function', help='The evaluation function for ai agent.',
                        default='score_evaluation_function', type=str)
    args = parser.parse_args()
    numpy.random.seed(args.random_seed)

    agent = create_agent(args)
    game_runner = GameRunner(agent, sleep_between_actions=args.sleep_between_actions)
    deck = Deck()
    initial_state = GameState(deck)
    won_games = 0

    for i in range(args.num_of_games):
        looser = game_runner.new_game(initial_state)
        if type(looser) is RandomOpponentAgent:
            won_games += 1
        print("looser is ", looser)

    print(f"You won {won_games}/{args.num_of_games} games ")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
