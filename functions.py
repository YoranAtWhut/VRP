# -*- coding: utf-8 -*-

import math

def _distance_between_nodes(node1_pos,node2_pos):
    diff = node1_pos-node2_pos
    return math.sqrt(diff.dot(diff))

def _cal_one_vehicle_distance_time(nodes,route,route_id):
    sorted_route = list(route.items())
    vehicle_info = nodes.vehicles[route_id]
    velocity = vehicle_info['velocity']
    dep_node = vehicle_info['dep_node']
    ari_node = vehicle_info['ari_node']
    start_node_pos = nodes.get_node_from_id(dep_node).get_pos()
    end_node_pos = nodes.get_node_from_id(ari_node).get_pos()
    
    total_distance = 0.0
    total_time = 0.0
    
    pre_pos = start_node_pos
    for element in sorted_route:
        next_pos = nodes.get_node_from_id(element[1]).get_pos()
        distance = _distance_between_nodes(pre_pos,next_pos)
        total_distance += distance
        total_time += distance/velocity
        total_time += nodes.get_node_from_id(element[1]).get_service_time()
        pre_pos = next_pos
    next_pos = end_node_pos
    total_distance += _distance_between_nodes(pre_pos,next_pos)
    total_time += _distance_between_nodes(pre_pos,next_pos)/velocity
    
    return total_distance,total_time

def _time_between_nodes(node1_pos,node2_pos,velocity):
    return _distance_between_nodes(node1_pos,node2_pos)/velocity

def calc_distance_time(nodes,individual):
    if not individual.distance:
        chromosome = individual.chromosome
        total_distance = 0.0
        total_time = 0.0
        for route_id,route in enumerate(chromosome):
            distance,time = _cal_one_vehicle_distance_time(nodes,route,route_id)
            total_distance += distance
            total_time += time
        individual.time = total_time
        individual.distance = total_distance
        return total_distance,total_time
    else:
        return individual.distance,individual.time

def _cal_fitness(nodes,candidate):
    candidate.distance,candidate.time = calc_distance_time(nodes,candidate)
    fitness = 10000/(5*candidate.distance + 50 * candidate.time)
    candidate.fitness = fitness
    return fitness

def community_fitness(nodes,parents):
    com_fitness = []
    for individual in parents:
        individual_id = individual.id
        individual_fitness = _cal_fitness(nodes,individual)
        com_fitness.append((individual_id,individual_fitness))
    return com_fitness

def remove_null_route(chromosome):
    return [route for route in chromosome if len(route)!=0]