import argparse

from Logger import Logger
import numpy
import pygame
from Multi_Agents import *
from Deck import Deck
from Game import Game, RandomOpponentAgent
from GameState import GameState
from Constants import *
import util


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
        self._agent.hand = []
        self._agent.extend_hand(ag_hand)
        game = Game(self._agent, opponent_agent,
                    sleep_between_actions=self.sleep_between_actions)
        self.current_game = game
        return game.run(initial_state, self.screen)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


def create_agent(args, weights=None):
    if args.agent == "ExpectimaxAgent":
        agent = ExpectimaxAgent(depth=args.depth)
    elif args.agent == "KeyboardAgent":
        agent = KeyboardAgent()
    elif args.agent == "MinimaxAgent":
        agent = MinmaxAgent(depth=args.depth)
    elif args.agent == "AlphaBetaAgent":
        agent = AlphaBetaAgent(depth=args.depth)
    elif args.agent == "GeneticAgent":
        agent = GeneticAgent(weights)

        # get current weight vector
        # with open(WEIGHT_VECTOR, 'rb') as f:
        #     data = pickle.load(f)
        #     self.vector1 = data[0]
        #     self.vector2 = data[1]
        # with open(WINS_LAST_ITER, 'rb') as f:
        #     self.last_game_wins = pickle.load(f)
    return agent


def create_offspring(p1: Counter, p2: Counter, args):
    offspring = copy.copy(p1)
    for i in offspring:
        if util.flipCoin(0.5):
            offspring[i] = p2[i]
        if util.flipCoin(args.mutation_coef):
            Logger.info("A mutation has occurred!!!")
            print("A mutation has occurred!!!")
            if util.flipCoin(0.5):
                offspring[i] *= args.mutation_strength
            else:
                offspring[i] /= args.mutation_strength
    Logger.info(str(offspring))
    print(offspring)
    return offspring


def create_offsprings(args, parentA, parentB):
    little_shits = []
    for i in range(args.num_of_offsprings):
        little_shits.append(create_offspring(parentA, parentB, args))
    return little_shits


def main():
    parser = argparse.ArgumentParser(description='Durak game.')
    parser.add_argument('--random_seed', help='The seed for the random state.',
                        default=numpy.random.randint(100),
                        type=int)
    agents = ["KeyboardAgent", 'ExpectimaxAgent', "MinimaxAgent",
              "AlphaBetaAgent", "GeneticAgent"]
    parser.add_argument('--agent', choices=agents, help='The agent.',
                        default=agents[4], type=str)
    parser.add_argument('--depth',
                        help='The maximum depth for to search in the game tree.',
                        default=2, type=int)
    parser.add_argument('--sleep_between_actions',
                        help='Should sleep between actions.', default=False,
                        type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.',
                        default=2, type=int)
    parser.add_argument('--num_of_generations',
                        help='The number of generations to run.',
                        default=3, type=int)
    parser.add_argument('--num_of_offsprings',
                        help='The number of offsprings to spawn.',
                        default=2, type=int)
    parser.add_argument('--mutation_coef',
                        help='Chance of a mutation occuring.',
                        default=0.05, type=int)
    parser.add_argument('--mutation_strength',
                        help='Strength of a mutation.',
                        default=2, type=int)
    parser.add_argument('--evaluation_function',
                        help='The evaluation function for ai agent.',
                        default='score_evaluation_function', type=str)
    parser.add_argument('--opponent',
                        help='Opponent to play against',
                        default='RandomOpponentAgent', type=str)

    args = parser.parse_args()
    numpy.random.seed(args.random_seed)

    if args.agent == "GeneticAgent":
        parentA, parentB = Counter(), Counter()
        calculate_weights(parentA, 2)
        calculate_weights(parentB, 0.5)

        for gen in range(args.num_of_generations):
            offspring_score = dict()
            for ind, offspring in enumerate(
                    create_offsprings(args, parentA, parentB)):
                agent = GeneticAgent(offspring)
                score = run_games(args, agent)
                offspring_score[ind] = (offspring, score)
            sorted(offspring_score.items(), key=lambda item: item[1][1])
            data = list(offspring_score.keys())
            parentA, parentB = offspring_score[data[0]][0], \
                               offspring_score[data[1]][0]
            score = offspring_score[data[0]][1]
            Logger.add_genetic_table_entry(seed=args.random_seed, num_of_games=args.num_of_games,
                                           num_of_generations=args.num_of_generations,
                                           num_of_offsprings=args.num_of_offsprings, mutation_coef=args.mutation_coef,
                                           mutation_strength=args.mutation_strength, current_gen=gen + 1, score=score)
            Logger.info("generation: " + str(gen + 1))
            print("generation: " + str(gen + 1))

        # get final offspring
        # for ind, offspring in enumerate([parentA, parentB]):
        #     agent = GeneticAgent(offspring)
        #     score = run_games(args, agent)
        #     offspring_score[ind] = (offspring, score)
        #     sorted(offspring_score.items(), key=lambda item: item[1][1])
        #     data = list(offspring_score.keys())
        # hes the best, around
        rocky, score = offspring_score[data[0]][0], offspring_score[data[0]][1]

        # with open(, 'wb') as f:
        #     pickle.dump(won_games, f)
        print("best score was: " + str(score))
        print(rocky)
        Logger.info("best score was: " + str(score) + "\n best rocky was " + str(rocky))
        Logger.write_to_log()
    else:
        agent = create_agent(args)
        run_games(args, agent)


def run_games(args, agent):
    game_runner = GameRunner(agent,
                             sleep_between_actions=args.sleep_between_actions)
    deck = Deck()
    initial_state = GameState(deck)
    initial_state.Opponent = args.opponent
    won_games = 0

    for i in range(args.num_of_games):
        Logger.info(f"Game #{i + 1}")
        looser = game_runner.new_game(initial_state)
        if type(looser) is RandomOpponentAgent:
            won_games += 1
        Logger.info(f"looser is {looser}")
        print("looser is ", looser)

    Logger.info(f"You won {won_games}/{args.num_of_games} games ")
    print(f"You won {won_games}/{args.num_of_games} games ")
    return won_games / args.num_of_games


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
