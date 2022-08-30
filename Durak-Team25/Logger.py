import os.path
from datetime import datetime
import pandas as pd


class Logger:
    now = datetime.now().strftime("%H-%M-%S")
    if not os.path.isdir("Logs"):
        os.mkdir("Logs")
    log = open(f"Logs/Log_{now}.txt", "a")
    columns = ["seed", "num_of_games", "num_of_generations", "num_of_offsprings", "mutation_coef",
               "mutation_strength", "current_gen", "score", "gen_score"]
    genetic_table = pd.DataFrame(columns=columns)
    alpha_table = pd.DataFrame(columns=["depth", "win_rate", "num_of_game", "Opponent"])
    expecti_table = pd.DataFrame(columns=["depth", "win_rate", "num_of_game", "Opponent"])

    @staticmethod
    def info(message: str):
        Logger.log.write(message + "\n")

    @staticmethod
    def add_genetic_table_entry(seed, num_of_games, num_of_generations, num_of_offsprings, mutation_coef,
                                mutation_strength, current_gen, score, gen_score):
        to_add = [seed, num_of_games, num_of_generations, num_of_offsprings, mutation_coef,
                  mutation_strength, current_gen, score, gen_score]
        Logger.genetic_table.loc[len(Logger.genetic_table)] = to_add

    @staticmethod
    def add_alpha_table_entry(seed,depth, win_rate, num_of_game, opponent):
        alpha_table = pd.DataFrame(columns=["depth", "win_rate", "num_of_game", "Opponent"])
        alpha_table.loc[len(alpha_table)] = [depth, win_rate, num_of_game, opponent]
        alpha_table.to_csv(f"Logs/AlphaBeta_{seed}", mode="a", index=False, header=False)

    @staticmethod
    def add_expecti_table_entry(seed, depth, win_rate, num_of_game, opponent):
        expecti_table = pd.DataFrame(columns=["depth", "win_rate", "num_of_game", "Opponent"])
        expecti_table.loc[len(expecti_table)] = [depth, win_rate, num_of_game, opponent]
        expecti_table.to_csv(f"Logs/Expectimax_{seed}", mode="a", index=False, header=False)

    @staticmethod
    def write_to_log():
        table = Logger.genetic_table
        log_name = f'{table["seed"][0]}_{table["num_of_games"][0]}_{table["num_of_generations"][0]}_{table["num_of_offsprings"][0]}_{table["mutation_coef"][0]}_{table["mutation_strength"][0]}'
        Logger.genetic_table.to_csv(f"Logs/GeneticTable_{log_name}.csv", sep=",")
        Logger.log.close()
