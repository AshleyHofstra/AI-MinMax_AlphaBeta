class HumanPlayer:
    def __init__(self, name):
        self.name = name 
    
    def chooseAction(self, state):
        row = input("Input your action row: ")
        if(row.lower() == "quit"):
            exit()
            return

        while True:
            try:
                row = int(row)
                
                col = int(input("Input your action col: "))

                action = (row, col)
                if action in state.availablePositions():
                    return action
                else:
                    print("That box has already been chosen, please try again.")
                    return self.chooseAction(state)
            except:
                print("There was a problem with your input, please try again.")
                return self.chooseAction(state)
            