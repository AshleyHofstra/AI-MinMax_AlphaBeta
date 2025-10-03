# Tic Tac Toe
#Two players against eachother

# x │ O │ O
#───┼───┼───
# O │ X │ X
#───┼───┼───
#   │   │ X

import numpy as np

BOARD_ROWS = 3
BOARD_COLS = 3

class State:
    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS)) #fill board with 0's
        self.boardHash = None #init hash to None
        
    def getHash(self):
        '''
        ### Summary:
        * Get unique hash of current board state
        ### Returns:
        * boardHash: string 2d array representing board
        '''
        self.boardHash = str(self.board.reshape(BOARD_COLS*BOARD_ROWS))
        return self.boardHash
    
    def winner(self):
        '''
        ### Summary:
        * Returns the winner and sets isEnd to True
        ### Returns:
        * -1 if p2 wins
        * 1 if p1 wins
        * 0 if tie
        '''
        # row
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        # col
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS-i-1] for i in range(BOARD_COLS)])
        if (diag_sum1 == 3 or diag_sum2 == 3):
            self.isEnd  = True
            return 1
        elif (diag_sum1 == -3 or diag_sum2 == -3):
            self.isEnd  = True
            return -1
        
        # tie
        # no available positions
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        # not end
        self.isEnd = False
        return None
    
    def availablePositions(self):
        '''
        ### Summary:
        * Checks for all available (vacant) positions
        ### Returns
        * Array of tuples indicating vacant positions in form (row, col)
        '''
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))  # need to be tuple
        return positions
    
    def updateState(self, position, playerSymbol):
        '''
        ### Summary:
        * Updates board state
        ### Parameters:
        * position: tuple of desired board square position
        '''
        self.board[position] = playerSymbol #Sets square to player's symbol
        # switch to another player
    
    # board reset
    def reset(self):
        '''
        ### Summary:
        * Resets game variables back to initial values
        '''
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
    

    def showBoard(self):
        # p1: x  p2: o

        print("    0   1   2")
        for i in range(0, BOARD_ROWS):
            print('  -------------')
            out = str(i) + ' | '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('  -------------')        


    def toString(self):
        strn = ""
        for i in range(0, BOARD_ROWS):
            strn += ('-------------\n')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            strn += (out) + "\n"
        strn += ('-------------\n')    
        return strn    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def play_against_human(self):
        '''
        ### Summary: 
        * minmax game
        * minmax/alphabeta is p1
        * human is p2
        '''
        while not self.isEnd: #loop until end of game reached
                # Player 1, ai chooses position
                p1_action = self.p1.chooseAction(self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                # check board status if it is end
                self.showBoard()

                win = self.winner()
                if win is not None: #winner ==> stp[]    
                    if win == 1:
                        print("Minmax/alphabeta wins")
                    elif win == -1:
                        print("Human wins")
                    else:
                        print("Tie")
                    self.reset() # starts a new game
                
                # player 2 = human
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)
                self.updateState(p2_action)
                self.showBoard()

                win = self.winner()
                if win is not None:     
                    if win == 1:
                        print("Minmax wins")
                    elif win == -1:
                        print("Human wins")
                    else:
                        print("Tie")
                    self.reset()


    # plays against another RL agent
    def play(self, rounds=100):
        p1_results = {'wins':0, 'ties':0, 'losses':0}   
        p2_results =  {'wins':0, 'ties':0, 'losses':0}
        for i in range(rounds):
            if i%1000 == 0 or rounds <= 10:
                print("Rounds {}".format(i))
                print("Player 1 ", p1_results)
                print("Player 2 ", p2_results)
                p1_results = {'wins':0, 'ties':0, 'losses':0} #  
                p2_results =  {'wins':0, 'ties':0, 'losses':0}
            while not self.isEnd:
                # Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                # take action and upate board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                # check board status if it is end

                win = self.winner()
                if win is not None:     
                    if win == 1:
                        p1_results['wins'] += 1
                        p2_results['losses'] +=1
                    elif win == -1:
                        p1_results['losses'] +=1
                        p2_results['wins'] += 1
                    else:
                        p1_results['ties'] +=1
                        p2_results['ties'] +=1
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)
                    
                    win = self.winner()
                    if win is not None:
                        if win == 1:
                            p1_results['wins'] += 1
                            p2_results['losses'] +=1
                        elif win == -1:
                            p1_results['losses'] +=1
                            p2_results['wins'] += 1
                        else:
                            p1_results['ties'] +=1
                            p2_results['ties'] +=1
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break
    
    # play one play 
    def play2(self):
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and upate board state
            self.updateState(p1_action)
            self.showBoard()
            # check board status if it is end
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)

                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break