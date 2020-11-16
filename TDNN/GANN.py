# -*- coding:utf-8 -*-

import sys
# sys.path.append('/Users/shuangliz/Desktop/TBMTunnelingParameterPrediction/TDNN/Genetic.py')
from TDNN import Genetic
from operator import itemgetter
import numpy as np


GEN_LENGTH = 3  # the gen num in one population
RETAIN = 0.4
SELECT = 0.2
MUTATION = 0.2
NB_GENS = 1  # the generation of GA


def evolutionary_NN(nb_gens):
    genome = Genetic.Genetic()
    population = genome.create_population(strength=GEN_LENGTH)
    max_score = []
    min_score = []
    avg_score = []
    for _ in range(nb_gens):
        accuracy_scores, new_population = \
            genome.evolve(population, retain=RETAIN, select=SELECT, mutation=MUTATION)
        # visualize scores of each generation
        max_score.append(accuracy_scores[0])
        min_score.append(accuracy_scores[-1])
        avg_score.append(np.mean(accuracy_scores))
        population = new_population
    # the final population is (probably) the fittest population
    trained_pop = [(genome.evaluate_fitness(member), member)
                   for member in population]
    # arrange members according to their fitness scores
    sorted_scores = sorted(trained_pop, key=itemgetter(0))
    r2_scores = [pair[0] for pair in sorted_scores]
    # complete the scores for all generations
    max_score.append(r2_scores[0])
    min_score.append(r2_scores[-1])
    avg_score.append(np.mean(r2_scores))
    # select the best member
    fittest_member = sorted_scores[0][1]
    # and print its parameters
    for param in genome.param_choices:
        print(param, ": ", fittest_member[param])
    print("Highest r2 score: ", r2_scores[0])


if __name__ == '__main__':
    np.random.seed(0)
    evolutionary_NN(NB_GENS)
