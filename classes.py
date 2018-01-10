# -*- coding: utf-8 -*-

class Individual(object):
    def __init__(self,id,chromosome):
        self.id = id
        self.chromosome = chromosome
        self.time = None
        self.distance = None
        self.fitness = None
        
    def __eq__(self,other):
        if other is None or type(self) != type(other):
            return False
        return self.chromosome == other.chromosome
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
    def get_nvehicle(self):
        nvehicle = len(self.chromosome)
        return nvehicle
    
class Node(object):
    def __init__(self,id_,type_,position,early,late,service_time,demand):
        self.id = id_
        self.type = type_
        self.position = position
        self.demand = demand
        self.early = early
        self.late = late
        self.service_time = service_time
    
    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def get_pos(self):
        return self.position
    
    def get_demand(self):
        return self.demand
    
    def get_early(self):
        return self.early
    
    def get_late(self):
        return self.late
    
    def get_service_time(self):
        return self.service_time
    
class NodeList(list):
    def __init__(self,vehicles):
        list.__init__(self)
        self.vehicles = vehicles
        self.depots = []
        self.is_first_get_depot = True
        
    def get_depot(self):
        if self.is_first_get_depot:
            for node in self:
                if node.get_type() == 0:
                    self.depots.append(node)
            self.is_first_get_depot = False
            return self.depots
        return self.depots
    
    def get_customers(self):
        return [customer for customer in self if customer.get_type()!=0]
    
    def get_customers_id_list(self):
        return [customer.id for customer in self if customer.type != 0]
    
    def get_deliver_customer_size(self):
        return len(self.get_customers())/2
    
    def get_node_from_id(self,id):
        for node in self:
            if node.get_id() == id:
                return node
            
    def time_between_nodes(self,node1_pos,node2_pos,velocity):
                import math
                diff = node1_pos-node2_pos
                distance = 0.0
                '''for single_dis in diff:
                    distance += single_dis**2'''
                distance = diff.dot(diff)
                distance = math.sqrt(distance)
                return distance/velocity
    
    def is_feasible_route(self,route,route_id):                        
        vehicle_info = self.vehicles[route_id]
        capacity = vehicle_info['capacity']
        early = vehicle_info['early']
        late = vehicle_info['late']
        velocity = vehicle_info['velocity']
        dep_node_id = vehicle_info['dep_node']
        ari_node_id = vehicle_info['ari_node']
        dep_node = self.get_node_from_id(dep_node_id)
        ari_node = self.get_node_from_id(ari_node_id)
        
        route_nodes_id = [node_id for (index,node_id) in route.items()]
        
        route_nodes = [self.get_node_from_id(node_id) for node_id in route_nodes_id]
        
        current_time = 0.0       
        pre_node = dep_node
        total_demand = 0.0
        for i,node in enumerate(route_nodes):
            next_node = node
            total_demand += node.demand
            current_time += self.time_between_nodes(pre_node.get_pos(),next_node.get_pos(),velocity)
            if current_time > next_node.late:
                return False
            if total_demand > capacity:
                return False
            current_time += next_node.service_time
            pre_node = node
        next_node = ari_node
        current_time += self.time_between_nodes(pre_node.get_pos(),next_node.get_pos(),velocity)
        if current_time>late-early:
            return False
        return True
    
    def is_feasible(self,chromosome):
        for i,route in enumerate(chromosome):
            if not self.is_feasible_route(route,i):
                return False
        return True
        
            
            