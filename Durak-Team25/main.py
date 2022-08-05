import argparse

import numpy

import Multi_Agents
from Deck import Deck
from Game import Game, RandomOpponentAgent
from GameState import GameState


class GameRunner(object):
    def __init__(self, agent):
        super(GameRunner, self).__init__()
        self._agent = agent
        self.current_game = None

    def new_game(self, initial_state, *args, **kw):
        self.quit_game()
        initial_state.reshuffle()
        op_hand = initial_state.deck.hand_out_cards(6)
        opponent_agent = RandomOpponentAgent(op_hand)
        ag_hand = initial_state.deck.hand_out_cards(6)
        self._agent.hand = ag_hand
        game = Game(self._agent, opponent_agent)
        self.current_game = game
        return game.run(initial_state)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


def create_agent(args):
    if args.agent == "ExpectimaxAgent":
        agent = Multi_Agents.ExpectimaxAgent()
    elif args.agent == "KeyboardAgent":
        agent = Multi_Agents.KeyboardAgent()
    return agent


def main():
    parser = argparse.ArgumentParser(description='Durak game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100),
                        type=int)
    # displays = ['GUI', 'SummaryDisplay']
    agents = ["KeyboardAgent", 'ExpectimaxAgent']
    # parser.add_argument('--display', choices=displays, help='The game ui.', default=displays[0], type=str)
    parser.add_argument('--agent', choices=agents, help='The agent.', default=agents[0], type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    # parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)

    parser.add_argument('--evaluation_function', help='The evaluation function for ai agent.',
                        default='score_evaluation_function', type=str)
    args = parser.parse_args()
    numpy.random.seed(args.random_seed)
    deck = Deck()
    initial_state = GameState(deck)
    # if args.display != displays[0]:
    #     display = util.lookup('displays.' + args.display, globals())()
    # else:
    #     display = None
    agent = create_agent(args)
    game_runner = GameRunner(agent)
    for i in range(args.num_of_games):
        winner = game_runner.new_game(initial_state)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
