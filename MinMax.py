from copy import deepcopy
from State import State
import numpy as np
import random as rand

class Node:
    def __init__(self, state, symbol, parent=None):
        self.state = state
        self.symbol = symbol #1 if is max turn, -1 if is min turn
        self.score = float('inf') * symbol * -1 #instantiate score to +/- infinity

        self.parent = parent
        self.children = {} #key is board hash

        self.nextAction = None

        self.action = None

class MinMaxPlayer:

    def __init__(self, name):
        self.name = name
        self.call = 0
    
    def minimax(self, node):
        self.call += 1

        #BASE CASE
        win = node.state.winner()
        if win is not None:
            node.score = win

        #RECURSIVE CASE
        else:
            positions = node.state.availablePositions()

            for pos in positions:
                #print(pos)
                childState = deepcopy(node.state) #copy board
                child = Node(childState, node.symbol*-1, node)
                child.state.updateState(pos, node.symbol) #make move
                child.action = pos

                node.children[childState.getHash()] = child # add as child
                self.minimax(child) #Recursive call

                #Set node score
                #   max                                                min
                if (node.symbol == 1 and child.score > node.score) or (node.symbol == -1 and child.score < node.score):
                    node.score = child.score
                    node.nextAction = child.action


        
    def chooseAction(self, state):
        #Run minimax with current board as root
        root = Node(state, 1)
        self.call = 0

        action = None
        if(state.getHash() == "[0. 0. 0. 0. 0. 0. 0. 0. 0.]"): #First turn, can choose randomly
            positions = state.availablePositions()
            action = rand.choice(positions)

        #Not first turn
        else:
            self.minimax(root) #calculate
            action = root.nextAction

        print("Calls: " + str(self.call))
        return action