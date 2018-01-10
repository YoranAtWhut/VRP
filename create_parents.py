# -*- coding: utf-8 -*-
import random
import copy

from classes import Individual
from data import loadDataSet

def create_individual(nodes,index):
    customers_id_list = nodes.get_customers_id_list()
    deliver_list = customers_id_list[:int(len(customers_id_list)/2)]
    n_vehicle = len(nodes.vehicles)
    
    def create_route_from_nodes(route_nodes):
        if len(route_nodes) != 0:
            route = []
            valid = []
            valid.append(route_nodes[0])
            for _ in range(len(route_nodes)*2):
                route.append(random.sample(valid,1)[0])
                the_last = route[-1]

                if the_last in route_nodes:
                    the_last_index_nodes = route_nodes.index(the_last)
                    if the_last_index_nodes < (len(route_nodes)-1):
                        valid.append(route_nodes[the_last_index_nodes+1])
                    valid.append(the_last+len(deliver_list))
                valid.remove(the_last)
            route = {(index+1):node_id for (index,node_id) in enumerate(route)}
        else:
            route = {}
        return route
    
    chromosome = []
    tmp_deliver_list = copy.deepcopy(deliver_list)
    customer_size = len(tmp_deliver_list)
    
    for i in range(n_vehicle-1):
        while True:
            limitation = min(30,len(tmp_deliver_list))
            min_val = min(2,limitation)
            max_val = max(2,limitation)
            route_nodes_size = random.randint(min_val,max_val)
            if limitation <= 1:
                route_nodes_size = len(tmp_deliver_list)
            if i>=12:
                route_nodes_size = random.randint(0,limitation)
            route_nodes = random.sample(tmp_deliver_list,route_nodes_size)
            route = create_route_from_nodes(route_nodes)
            
            if not nodes.is_feasible_route(route,i):
                continue
            else:
                tmp_deliver_list = [element for element in tmp_deliver_list if element not in route_nodes]
                break
        chromosome.append(route)
        customer_size = customer_size - route_nodes_size
        
    j = 0
    while True:
        j += 1
        if j > 200:
            return None
        route_nodes = random.sample(tmp_deliver_list,len(tmp_deliver_list))
        route = create_route_from_nodes(route_nodes)
        if nodes.is_feasible_route(route,i+1):
            break
    chromosome.append(route)
    individual = Individual(index,chromosome)
    return individual

def create_parents(POPULATION,nodes):
    #nodes = loadDataSet('data5.xml')
    index = 1
    parents = []
    while True:
        print(index)
        individual = create_individual(nodes,index)
        if not individual:
            pass
        else:
            index += 1
            parents.append(individual)
        if index >= POPULATION:
            break
    return parents
            

if __name__ == '__main__':
    nodes = loadDataSet('data5.xml')
    parents = create_parents(200,nodes)
    import pickle
    parents_file = open('parents.txt','wb')
    
    pickle_string = pickle.dumps(parents)
    parents_file.write(pickle_string)
    parents_file.close()
    '''for indvidual in parents:
        print(indvidual.id)
        #print(indvidual.chromosome,len(indvidual.chromosome))
        lengths = [len(indvidual.chromosome[i]) for i in range(len(indvidual.chromosome))]
        print(lengths.count(0))
        if lengths.count(0) > 1:            
            print('length',sum(lengths),lengths.count(0))
            print(indvidual.chromosome)'''
    '''import crossover,mutation
    nodes = loadDataSet('data5.xml')
    offspirngs = crossover.crossover(nodes,parents)
    offsprings = mutation.mutation_community(nodes,offspirngs)'''