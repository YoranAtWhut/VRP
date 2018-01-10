# -*- coding: utf-8 -*-
import random
import copy

from functions import remove_null_route
from data import loadDataSet

def mutation_route(nodes,route):
    route_nodes = list(route.values())
    deliver_size = nodes.get_deliver_customer_size()
    while True:
        change_node_1 = random.sample(route_nodes,1)[0]
        change_node_1_id = change_node_1 if change_node_1 <= deliver_size else change_node_1 - deliver_size
        tmp = copy.deepcopy(route_nodes)
        change_node_2_id = random.sample(tmp,1)[0]
        if change_node_2_id == change_node_1_id or change_node_2_id == (change_node_1_id + deliver_size):
            # print('dead loop',change_node_2_id,change_node_1_id)
            continue
        change_node_1_index = tmp.index(change_node_1_id)
        change_node_2_index = tmp.index(change_node_2_id)
        tmp_node = tmp[change_node_1_index]
        tmp[change_node_1_index] = tmp[change_node_2_index]
        tmp[change_node_2_index] = tmp_node
        change_node_2_id = change_node_2_id if change_node_2_id <= deliver_size else change_node_2_id-deliver_size
        if tmp.index(change_node_2_id) >= tmp.index(change_node_2_id+deliver_size):
            continue
        elif tmp.index(change_node_1_id) >= tmp.index(change_node_1_id+deliver_size):
            continue
        else:
            break
    route = {(index + 1): node_id for (index, node_id) in enumerate(tmp)}
    return route
'''
def mutation_chromosome(nodes,chromosome):
    for i,route in enumerate(chromosome):
        if random.random()>0.9:
            j = 0
            while True:
                j += 1
                print(j)
                new_route = mutation_route(nodes,route)
                if not nodes.is_feasible_route(new_route,i):
                    chromosome[i] = new_route
                    break
                if j > 200:
                    break
    return chromosome

def mutation_community(nodes,indv_list,pm=0.99):
    for indv in indv_list:
        if random.random()>pm:
            tmp_chromosome = mutation_chromosome(nodes,indv.chromosome)
            indv.chromosome = tmp_chromosome
    return indv_list
'''
def mutation_chromosome(nodes,chromosome):
    for i,route in enumerate(chromosome):
        if len(route) >=4:
            if random.random()>0.1:
                new_route = mutation_route(nodes,route)
                if nodes.is_feasible_route(new_route,i):                    
                    chromosome[i] = new_route
                    break
    return chromosome

def mutation_community(nodes,indv_list,pm=0.9):
    for indv in indv_list:
        if random.random()>pm:
            tmp_chromosome = mutation_chromosome(nodes,indv.chromosome)
            indv.chromosome = tmp_chromosome
    return indv_list

if __name__ == '__main__':

    nodes = loadDataSet('data5.xml')
    #print(len(nodes),nodes)

    chromosome1 = [{1: 7, 2: 37, 3: 9, 4: 39}, {1: 30, 2: 29, 3: 60, 4: 59, 5: 10, 6: 40}, {1: 3, 2: 6, 3: 33, 4: 5, 5: 35, 6: 36}, {1: 21, 2: 27, 3: 51, 4: 28, 5: 58, 6: 57}, {1: 2, 2: 14, 3: 44, 4: 32}, {1: 24, 2: 1, 3: 31, 4: 54}, {1: 20, 2: 11, 3: 41, 4: 50}, {1: 13, 2: 25, 3: 55, 4: 43}, {1: 15, 2: 17, 3: 45, 4: 47}, {1: 12, 2: 26, 3: 56, 4: 42}, {1: 18, 2: 4, 3: 48, 4: 34}, {1: 19, 2: 23, 3: 49, 4: 53}, {1: 16, 2: 46}, {1: 22, 2: 52}, {1: 8, 2: 38}]
    chromosome2 = [{1: 2, 2: 1, 3: 7, 4: 5, 5: 8, 6: 11, 7: 6, 8: 12, 9: 4, 10: 3, 11: 10, 12: 9}, {}]
    chromosome3 = [{1: 2, 2: 8}, {1: 3, 2: 6, 3: 1, 4: 12, 5: 9, 6: 5, 7: 4, 8: 11, 9: 7, 10: 10}]
    chromosome4 = [{}, {1: 2, 2: 1, 3: 7, 4: 5, 5: 8, 6: 11, 7: 6, 8: 12, 9: 4, 10: 3, 11: 10, 12: 9}]
    route = {1: 1, 2: 4, 3: 7, 4: 10, 5: 6, 6: 12, 7: 5, 8: 11}

    print(mutation_chromosome(nodes,chromosome1))