import os.path
from datetime import datetime
import pandas as pd


class Logger:
    now = datetime.now().strftime("%H-%M-%S")
    if not os.path.isdir("Logs"):
        os.mkdir("Logs")
    log = open(f"Logs/Log_{now}.txt", "a")
    columns = ["seed", "num_of_games", "num_of_generations", "num_of_offsprings", "mutation_coef",
               "mutation_strength", "current_gen", "score"]
    genetic_table = pd.DataFrame(columns=columns)

    @staticmethod
    def info(message: str):
        Logger.log.write(message + "\n")

    @staticmethod
    def add_genetic_table_entry(seed, num_of_games, num_of_generations, num_of_offsprings, mutation_coef,
                                mutation_strength, current_gen, score):
        to_add = [seed, num_of_games, num_of_generations, num_of_offsprings, mutation_coef,
                  mutation_strength, current_gen, score]
        Logger.genetic_table.loc[len(Logger.genetic_table)] = to_add

    @staticmethod
    def write_to_log():
        table = Logger.genetic_table
        log_name = f'{table["seed"][0]}_{table["num_of_games"][0]}_{table["num_of_generations"][0]}_{table["num_of_offsprings"][0]}_{table["mutation_coef"][0]}_{table["mutation_strength"][0]}'
        Logger.genetic_table.to_csv(f"Logs/GeneticTable_{log_name}.csv", sep=",")
        Logger.log.close()
