from genetic_algorithm import GeneticAlgorithm
from game_manager import GameManager
from player import BasePlayer
from advanced_player import AdvancedPlayer
import numpy as np
import pickle
import time


def fitness_evaluator(array):
    base_player_list = [BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
    gm = GameManager([AdvancedPlayer('A', array)] + base_player_list)
    scores_dict, draw_count = gm.play_games(100)
    if draw_count > 100:
        return -np.inf
    return min(scores_dict['B'], scores_dict['C'], scores_dict['D']) - scores_dict['A']

start_time = time.time()
ga = GeneticAlgorithm(142, fitness_evaluator, 100, 200, mutation_rate=0.25, mutation_severity=0.1)
vec = ga.evolve()
with open(time.strftime('%m%d%H%M')+'.p', 'wb') as f:
    pickle.dump(vec, f)
print(f'Time: {time.time() - start_time} s')