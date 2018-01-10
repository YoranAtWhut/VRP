# -*- coding: utf-8 -*-

import random
import copy
import numpy as np

from data import loadDataSet
from functions import remove_null_route
from classes import Individual

def exchange_chromosome(nodes,ch1):
    deliver_size = nodes.get_deliver_customer_size()
    no_Null_Chromosome = copy.deepcopy(remove_null_route(ch1))
    
    if len(no_Null_Chromosome)==15:
        if random.random()>0.5:
            # two route exchange
            two_index = random.sample(range(0,len(no_Null_Chromosome)),2)
            route1 = no_Null_Chromosome[two_index[0]]
            route2 = no_Null_Chromosome[two_index[1]]
            raw_index1 = ch1.index(route1)
            raw_index2 = ch1.index(route2)
            reversed_route_1 = {node_id:index for (index,node_id) in route1.items()}
            reversed_route_2 = {node_id: index for (index, node_id) in route2.items()}
            route_deliver_nodes_1 = np.sort(np.array(list(reversed_route_1.keys())))[:int(len(reversed_route_1)/2)]
            route_deliver_nodes_2 = np.sort(np.array(list(reversed_route_2.keys())))[:int(len(reversed_route_2) / 2)]
            exchange_start_node_1 = random.sample(route_deliver_nodes_1.tolist(), 1)[0]
            exchange_start_node_2 = random.sample(route_deliver_nodes_2.tolist(), 1)[0]
            exchange_end_node_1 = exchange_start_node_1 + deliver_size
            exchange_end_node_2 = exchange_start_node_2 + deliver_size
            tmp = route1[reversed_route_1[exchange_start_node_1]]
            route1[reversed_route_1[exchange_start_node_1]] = route2[reversed_route_2[exchange_start_node_2]]
            route2[reversed_route_2[exchange_start_node_2]] = tmp
            tmp = route1[reversed_route_1[exchange_end_node_1]]
            route1[reversed_route_1[exchange_end_node_1]] = route2[reversed_route_2[exchange_end_node_2]]
            route2[reversed_route_2[exchange_end_node_2]] = tmp
            ch1[raw_index1] = route1
            ch1[raw_index2] = route2
        else:
            # delete elements of one route and add them to another route
            two_index = random.sample(range(0, len(no_Null_Chromosome)), 2)
            route1 = no_Null_Chromosome[two_index[0]]
            route2 = no_Null_Chromosome[two_index[1]]
            raw_index1 = ch1.index(route1)
            raw_index2 = ch1.index(route2)
            route_nodes_1 = list(route1.values())
            route_nodes_2 = list(route2.values())
            exchange_node1 = random.sample(route_nodes_1, 1)[0]
            if exchange_node1 <= deliver_size:
                exchange_start_node_1 = exchange_node1
                exchange_end_node_1 = exchange_node1 + deliver_size
            else:
                exchange_start_node_1 = exchange_node1 - deliver_size
                exchange_end_node_1 = exchange_node1
            route_nodes_1.remove(exchange_start_node_1)
            route_nodes_1.remove(exchange_end_node_1)
            route2_size = len(route_nodes_2)
            random_insert = random.randint(0, route2_size)
            route_nodes_2.insert(random_insert, exchange_start_node_1)
            insert_index = route_nodes_2.index(exchange_start_node_1)
            route_nodes_2.insert(random.randint(insert_index + 1, len(route_nodes_2)), exchange_end_node_1)
            route1 = {(i + 1): int(node_id) for (i, node_id) in enumerate(route_nodes_1)}
            route2 = {(i + 1): int(node_id) for (i, node_id) in enumerate(route_nodes_2)}
            ch1[raw_index1] = route1
            ch1[raw_index2] = route2
    elif len(no_Null_Chromosome)<15 and random.random()>0.9:
        route = no_Null_Chromosome[0]
        lengths = [len(ch1[i]) for i in range(len(ch1))]
        raw_index = ch1.index(route)
        route_nodes = list(route.values())
        exchange_node = random.sample(route_nodes, 1)[0]
        if exchange_node <= deliver_size:
            exchange_start_node_1 = exchange_node
            exchange_end_node_1 = exchange_node + deliver_size
        else:
            exchange_start_node_1 = exchange_node - deliver_size
            exchange_end_node_1 = exchange_node
        route_nodes.remove(exchange_start_node_1)
        route_nodes.remove(exchange_end_node_1)
        route = {(index + 1): node_id for index, node_id in enumerate(route_nodes)}
        ch1[raw_index] = route
        added_route = [exchange_start_node_1, exchange_end_node_1]
        added_route = {(index + 1): int(node_id) for index, node_id in enumerate(added_route)}
        add_index = lengths.index(0)
        '''if raw_index == 0:
            ch1[raw_index + 1] = added_route
        elif raw_index == (len(ch1) - 1):
            ch1[raw_index - 1] = added_route
        else:
            ch1[raw_index + 1] = added_route'''
        ch1[add_index] = added_route
    
    return ch1

def crossover(nodes,parents,pc=0.7):
    offsprings = []
    for i,indv in enumerate(parents):
        if random.random() > pc:
            while True:
                tmp = copy.deepcopy(indv)
                chromosome = exchange_chromosome(nodes,tmp.chromosome)
                if nodes.is_feasible(chromosome):
                    break
            offspring = Individual(i+1,chromosome)
        else:
            offspring = Individual(i+1,indv.chromosome)
        offsprings.append(offspring)
    return offsprings

if __name__ == '__main__':
    nodes = loadDataSet('data5.xml')
    chromosome1 = [{1: 1, 2: 4, 3: 7, 4: 10, 5: 6, 6: 12, 7: 5, 8: 11}, {1: 2, 2: 8, 3: 3, 4: 9}]
    chromosome2 = [{1: 2, 2: 1, 3: 7, 4: 5, 5: 8, 6: 11, 7: 6, 8: 12, 9: 4, 10: 3, 11: 10, 12: 9}, {}]
    chromosome3 = [{1: 28, 2: 58, 3: 20, 4: 9, 5: 13, 6: 43, 7: 39, 8: 50}, {1: 2, 2: 15, 3: 45, 4: 32}, {1: 3, 2: 33, 3: 5, 4: 10, 5: 21, 6: 40, 7: 51, 8: 35}, {1: 18, 2: 7, 3: 48, 4: 37}, {1: 30, 2: 24, 3: 60, 4: 54}, {1: 16, 2: 46, 3: 12, 4: 42}, {1: 27, 2: 57, 3: 14, 4: 44}, {1: 25, 2: 19, 3: 23, 4: 55, 5: 53, 6: 49}, {1: 11, 2: 29, 3: 59, 4: 41}, {1: 17, 2: 1, 3: 31, 4: 47}, {1: 4, 2: 8, 3: 38, 4: 34}, {1: 26, 2: 6, 3: 36, 4: 56}, {}, {1: 22, 2: 52}, {}]
    chromosome4 = [{},{1: 2, 2: 1, 3: 7, 4: 5, 5: 8, 6: 11, 7: 6, 8: 12, 9: 4, 10: 3, 11: 10, 12: 9}]
    new_chromosome = exchange_chromosome(nodes,chromosome3)
    lengths = [len(new_chromosome[i]) for i in range(len(new_chromosome))]
    print(sum(lengths))
    print(len(new_chromosome))
    print(new_chromosome)       