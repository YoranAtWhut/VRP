# -*- coding: utf-8 -*-
import random
import numpy as np

from classes import Individual
from data import loadDataSet
import functions

def pareto_ranking(nodes,parents,factor=10):
    community_fitness = functions.community_fitness(nodes,parents)
    offsprings = []
    fitnesses = [element[1] for element in community_fitness]
    fitnesses = fitnesses/np.sum(fitnesses)
    
    def random_pick(some_list,probabilities):
        x = random.uniform(0,1)
        cumulative_probability = 0.0
        for item,item_probability in zip(some_list,probabilities):
            cumulative_probability += item_probability
            if x < cumulative_probability:break
        return item
    
    for i in range(len(parents)):
        offspring = random_pick(parents,fitnesses)
        offspring = Individual(i+1,offspring.chromosome)
        offsprings.append(offspring)
    
    return offsprings