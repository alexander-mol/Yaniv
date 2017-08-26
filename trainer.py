from genetic_algorithm import GeneticAlgorithm
from game_manager import GameManager
from player import BasePlayer
from advanced_player import AdvancedPlayer
import numpy as np
import pickle
import time


def fitness_evaluator(array):
    num_estimates = 10000
    base_player_list = [BasePlayer('B'), BasePlayer('C'), BasePlayer('D')]
    gm = GameManager([AdvancedPlayer('A', array)] + base_player_list)
    scores_dict, draw_count = gm.play_games(num_estimates)
    for key in scores_dict:
        scores_dict[key] /= num_estimates
    draw_rate = draw_count / num_estimates
    if draw_rate > 0.1:
        return -np.inf
    return min(scores_dict['B'], scores_dict['C'], scores_dict['D']) - scores_dict['A']

start_time = time.time()
ga = GeneticAlgorithm(27, fitness_evaluator, 50, 100, mutation_rate=0.2, mutation_severity=0.1, use_parallelism=True)
vec = ga.evolve()
with open(time.strftime('%m%d%H%M')+'.p', 'wb') as f:
    pickle.dump(vec, f)
print(f'Time: {time.time() - start_time} s')
