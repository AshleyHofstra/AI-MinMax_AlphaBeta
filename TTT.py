from State import State
from Human import HumanPlayer
from MinMax import MinMaxPlayer
from AlphaBeta import AlphaBetaPlayer
from RandomPlayer import RandomPlayer

import matplotlib.pyplot as plt
import numpy as np


class Game:
    def __init__(self):
        self.board = State()
        self.p1 = None # minimax or alphabeta
        self.p2 = None # human
        self.isEnd = False # game not yet ended
        self.count = 0

        self.data = {}

        # init p1 plays first
        self.playerSymbol = 1

        self.wins = {
            1: 0,   #p1
            -1: 0,  #p2
            0: 0}   #ties

    def play_against_human(self, model):
        if(model == "MinMax"):
            self.p1 = MinMaxPlayer(model)
        else:
            self.p1 = AlphaBetaPlayer(model)
    

        self.p2 = HumanPlayer("Human")
        
        self.board.reset()
        self.isEnd = False
        self.playerSymbol = 1

        players = {1: self.p1, -1: self.p2}

        self.count += 1
        self.data["Game " + str(self.count)] = {}

        print("Game " + str(self.count))

        roundNum = 0
        while not self.isEnd:

            curPlayer = players[self.playerSymbol]
            print("\n" + curPlayer.name + "'s Turn")

            action = curPlayer.chooseAction(self.board)
            if(self.playerSymbol == 1):
                roundNum += 1
                self.data["Game " + str(self.count)]["Round " + str(roundNum)] = curPlayer.call

            self.board.updateState(action, self.playerSymbol)
            self.board.showBoard()
            
            win = self.board.winner()
            if win is not None:   
                self.wins[win] += 1  
                if(win == 0):
                    print("Tie")
                else:
                    print(players[win].name + " wins")

                self.isEnd = True
                print(players[1].name + ": " + str(self.wins[1]))
                print(players[-1].name + ": " + str(self.wins[-1]))
                print("Ties: " + str(self.wins[0]))

            self.playerSymbol *= -1

    #For testing purposes
    def play_against_random(self, model):
        if(model == "MinMax"):
            self.p1 = MinMaxPlayer(model)
        else:
            self.p1 = AlphaBetaPlayer(model)
    

        self.p2 = RandomPlayer("Random")
        
        self.board.reset()
        self.isEnd = False
        self.playerSymbol = 1

        players = {1: self.p1, -1: self.p2}

        self.count += 1
        self.data["Game " + str(self.count)] = {}

        print("Game " + str(self.count))

        roundNum = 0
        while not self.isEnd:
            curPlayer = players[self.playerSymbol]

            action = curPlayer.chooseAction(self.board)
            if(self.playerSymbol == 1):
                roundNum += 1
                self.data["Game " + str(self.count)]["Round " + str(roundNum)] = curPlayer.call

            self.board.updateState(action, self.playerSymbol)
            
            win = self.board.winner()
            if win is not None:   
                self.board.showBoard()
                self.wins[win] += 1  
                if(win == 0):
                    print("Tie")
                else:
                    print(players[win].name + " wins")

                self.isEnd = True
                print(players[1].name + ": " + str(self.wins[1]))
                print(players[-1].name + ": " + str(self.wins[-1]))
                print("Ties: " + str(self.wins[0]))

            self.playerSymbol *= -1


game = Game()

choice = input("Choose a model\n1: MinMax\n2: AlphaBeta\n>>> ")

while(choice != "1" and choice != "2"):
    print("There was an error with your input. Please try again.")
    choice = input("Choose a model\n1: MinMax\n2: AlphaBeta\n>>> ")

models = {"1": "MinMax", "2": "AlphaBeta"}
model = models[choice]
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


'''
while(1):
    game.play_against_human(model)

    

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
'''

GAME_LIMIT = 10
while(game.count < GAME_LIMIT):
    game.play_against_human(model)
    
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


average = {}
getAvg = {}
avgStrn = "Averages: "

#Calc averages
for g in list(game.data.values()):
    for key, val in g.items():
        try:
            getAvg[key].append(val)
        except:
            getAvg[key] = [val]

for key, val in getAvg.items():
    average[key] = round(np.mean(val))
    avgStrn += "\n" + key + ": " + str(average[key])

#Plot
f = plt.figure()
for key, val in game.data.items():
    plt.scatter(list(val.keys()), list(val.values()), alpha=0.3, c="tab:blue")
plt.scatter(list(average.keys()), list(average.values()), alpha=0.75, c="tab:red")

plt.xlabel("Round Number")
plt.ylabel("Calls")
plt.title(model + " Calls per Round")

f.savefig("fig.png")
print(avgStrn)
print("Total: " + str(np.sum(list(average.values()))))