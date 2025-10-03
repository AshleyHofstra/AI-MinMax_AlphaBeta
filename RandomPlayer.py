import random as rand

class RandomPlayer:
    def __init__(self, name):
        self.name = name 
    
    def chooseAction(self, state):
        positions = state.availablePositions()
        return rand.choice(positions)        