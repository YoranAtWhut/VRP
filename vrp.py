# -*- coding: utf-8 -*-

import numpy as np

from classes import Individual
from data import loadDataSet
from functions import calc_distance_time,community_fitness,_cal_fitness
from create_parents import create_parents
from selection import pareto_ranking
from crossover import crossover
from mutation import mutation_community

POPULATION = 200
GSPAN = 200

def set_distance_time_fitness(nodes,parents):
    for individual in parents:
        calc_distance_time(nodes,individual)
        _cal_fitness(nodes,individual)

def remove_duplication(parents):
    nodupl_list = [parents[0]]
    for indv1 in parents[1:]:
        flag_add = True
        for indv2 in nodupl_list:
            if indv1 == indv2:
                flag_add = False
                break
        if flag_add:
            nodupl_list.append(indv1)
    return nodupl_list

def print_log(nodes,generation,parents):
    print('### Best Solutions of Generation'+str(generation)+'###')
    fitness_tuples = community_fitness(nodes,parents)
    max_fitness_index = [element[1] for element in fitness_tuples].index(
            max([element[1] for element in fitness_tuples]))
    best_solution = parents[max_fitness_index]
    fitness_mean = np.array([element[1] for element in fitness_tuples]).mean()
    print(best_solution.fitness,best_solution.distance,best_solution.time)
    print('best_solution_chromosome',best_solution.chromosome)
    print('mean',fitness_mean)
    return best_solution

def offsprings_fitness(nodes,offsprings,string):
    fitnesses = community_fitness(nodes,offsprings)
    fitness_mean = np.array([element[1] for element in fitnesses]).mean()
    return fitness_mean

def does_end(loopcount):
    if loopcount > GSPAN:
        return True
    return False

def main(filename='data5.xml'):
    import pickle
    print('#== LOADING DATASET FROM'+filename+"==#")
    nodes = loadDataSet(filename)
    #parents = create_parents(POPULATION,nodes)
    parents_file = open('parents.txt','rb')
    ps = parents_file.read()
    parents = pickle.loads(ps)
    parents_file.close()
    
    '''
    for individual in parents:
        print(individual.id)
        print(individual.chromosome)
        print('-------------------------')
    '''
    set_distance_time_fitness(nodes,parents)
    
    loopcount = 0
    pre_fitness_mean = offsprings_fitness(nodes,parents,'start')
    
    while not does_end(loopcount):
        while True:
            offsprings = pareto_ranking(nodes,parents,factor=1)
            fitness_mean = offsprings_fitness(nodes,offsprings,'selection')
            if fitness_mean > pre_fitness_mean:
                pre_fitness_mean = fitness_mean
                break
    
        while True:
            offsprings = crossover(nodes,offsprings,0.9)
            fitness_mean = offsprings_fitness(nodes,offsprings,'crossover')
            #if fitness_mean>pre_fitness_mean-0.001:
            if True:
                pre_fitness_mean = fitness_mean
                break
        
        offsprings = mutation_community(nodes,offsprings,0.99)
        fitness_mean = offsprings_fitness(nodes,offsprings,'mutation')
        
        parents = offsprings
        set_distance_time_fitness(nodes,parents)
        loopcount += 1
        print_log(nodes,loopcount,parents)
        
    
    '''while not does_end(loopcount):
        offsprings = pareto_ranking(nodes,parents,factor=1)
        offsprings = crossover(nodes,offsprings,0.9)
        offsprings = mutation_community(nodes,offsprings,0.99)'''
        
        
        
        
        
    
    best_solution = print_log(nodes,'final',parents)
    print(best_solution.fitness)
    
if __name__ == '__main__':
    main()