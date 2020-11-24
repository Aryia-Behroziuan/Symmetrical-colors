# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import unittest
import datetime
import genetic

def load_data(localFileName):
    
    with open(localFileName, mode='r') as infile:
        reader = csv.reader(infile)
        lookup = {row[0]: row[1].split(';') for row in reader if row}
    return lookup

class Rule:
    Node = None
    Adjacent = None
    
    def __init__(self, node, adjacent):
        if node < adjacent:
            node, adjacent = adjacent, node
        self.Node = node
        self.Adjacent = adjacent
        
    def __eq__(self, other):
        return self.Node == other.Node and \
                self.Adjacent == other.Adjacent 
                
    def __hash__(self):
        return hash(self.Node) * 397 ^ hash(self.Adjacent)

    def __str__(self):
        return self.Node + " -> " + self.Adjacent 
    
    def IsValid(self, genes, nodeIndexLookup):
        index = nodeIndexLookup[self.Node]
        adjacentStateIndex = nodeIndexLookup[self.Adjacent]
        return genes[index] != genes[adjacentStateIndex]

def build_rules(items):
    rulesAdded = {}
    
    for state, adjacent in items.items():
        for adjacentState in adjacent:
            if adjacentState == '':
                continue
            rule = Rule(state, adjacentState)
            if rule in rulesAdded:
                rulesAdded[rule] += 1
            else:
                rulesAdded[rule] = 1
                
                
    for k, v in rulesAdded.items():
        if v != 2:
            print("rule {0} is not bidirectional".format(k))
            
    return rulesAdded.keys()  

class GraphColoringTests(unittest.TestCase):
    def test(self):
        states = load_data("iran.csv")
        rules = build_rules(states)
        optimalValue = len(rules)
        stateIndexLookup = {key: index
                            for index, key in enumerate(sorted(states))}
        colors = ['Blue', 'Red', 'Green', 'Yellow']
        colorLookup = {color[0]: color for color in colors}
        geneset = list(colorLookup.keys())
        
        startTime = datetime.datetime.now()
        
        def fnDisplay(candidate):
            display(candidate, startTime)
            
        def fnGetFitness(genes):
            return get_fitness(genes, rules, stateIndexLookup)
        
        best = genetic.get_best(fnGetFitness, len(states), optimalValue,
                                geneset, fnDisplay)
        self.assertTrue(not optimalValue > best.Fitness)
        
        keys = sorted(states.keys())
        for index in range(len(states)):
            print(keys[index] + " is " + colorLookup[best.Genes[index]])
            
def display(candidate, startTime):
    timeD = datetime.datetime.now() - startTime
    print("{0}\t{1}\t{2}".format(
            ''.join(map(str, candidate.Genes)),
            candidate.Fitness,
            str(timeD)))   

def get_fitness(genes, rules, stateIndexLookup):
    rulesThatPass = sum(1 for rule in rules
                        if rule.IsValid(genes, stateIndexLookup)) 
    return rulesThatPass        
            
if __name__ == '__main__':
    unittest.main()            

    
                 
                 
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        