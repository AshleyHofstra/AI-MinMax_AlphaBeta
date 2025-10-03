from copy import deepcopy
from State import State
import numpy as np
import random as rand
from MinMax import MinMaxPlayer

class Node:
    def __init__(self, state, symbol, alpha=-1*float("inf"), beta=float("inf"), parent=None):
        self.state = state
        self.symbol = symbol #1 if is max turn, -1 if is min turn
        self.parent = parent

        self.children = {} #key is board hash
        self.action = None
        self.nextAction = None

        self.score = None
        self.alpha = alpha
        self.beta = beta

class AlphaBetaPlayer(MinMaxPlayer):
    def alphabeta(self, node):
        self.call += 1

        #BASE CASE
        win = node.state.winner()
        if win is not None:
            node.score = win
            node.alpha = None #For debugging purposes
            node.beta = None

        #RECURSIVE CASE
        else:
            positions = node.state.availablePositions()

            for pos in positions:
                childState = deepcopy(node.state) #copy board
                childState.updateState(pos, node.symbol) #make move

                #            child board, flip min/max, alpha,      beta,      parent
                child = Node(childState, node.symbol*-1, node.alpha, node.beta, node)
                child.action = pos
                
                node.children[childState.getHash()] = child # add as child

                self.alphabeta(child) #Recursive Call

                #max, adjust alpha
                if (node.symbol == 1 and child.score > node.alpha):
                    node.alpha = child.score
                    node.nextAction = child.action
                #min, adjust beta
                elif (node.symbol == -1 and child.score < node.beta):
                    node.beta = child.score
                    node.nextAction = child.action

                #Prune?
                if(node.beta <= node.alpha):
                    self.pruned += 1
                    break

            #Set score
            if(node.symbol == 1):
                node.score = node.alpha
            else:
                node.score = node.beta


    def chooseAction(self, state):
        root = Node(state, 1) #board, max, -inf, inf, no parent
        self.call = 0
        self.pruned = 0

        action = None
        if(state.getHash() == "[0. 0. 0. 0. 0. 0. 0. 0. 0.]"): #First turn, can choose randomly
            positions = state.availablePositions()
            action = rand.choice(positions)

        #Not first turn
        else:
            self.alphabeta(root) #calculate
            action = root.nextAction

        print("Calls: " + str(self.call))
        print("Pruned: " + str(self.pruned))
        return action