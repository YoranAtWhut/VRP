# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import numpy as np

from classes import Node,NodeList

def loadDataSet(filename='data.xml'):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    vehicles = []
    for vehicle in root.iter('vehicle'):
        vehicle_dict = {}
        vehicle_dict['id'] = int(vehicle.get('id'))
        vehicle_dict['dep_node'] = int(vehicle.find('departure_node').text)
        vehicle_dict['ari_node'] = int(vehicle.find('arrival_node').text)
        vehicle_dict['capacity'] = float(vehicle.find('capacity').text)
        vehicle_dict['early'] = float(vehicle.find('early').text)
        vehicle_dict['late'] = float(vehicle.find('late').text)
        vehicle_dict['velocity'] = float(vehicle.find('velocity').text)
        vehicles.append(vehicle_dict)
        
    nodes = NodeList(vehicles)
    
    for node,request in zip(root.iter('node'),root.iter('request')):
        id_ = int(node.get('id'))
        type_ = int(node.get('type'))
        x = float(node.find('cx').text)
        y = float(node.find('cy').text)
        position = np.array([x,y])
        early = float(node.find('early').text)
        late = float(node.find('late').text)
        service_time = float(node.find('s').text)
        demand = float(request.find('quantity').text)
        node_ = Node(id_,type_,position,early,late,service_time,demand)
        nodes.append(node_)
    
    return nodes

if __name__ == '__main__':
    nodes = loadDataSet('data5.xml')
    nodes.get_depot()