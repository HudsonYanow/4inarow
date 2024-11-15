import datetime

class Board:
    def __init__(self):
        self.currentBoard=[]
        for row in range(6):
            self.currentBoard.append([])
            for col in range(7):
                self.currentBoard[row].append(".")

    def printBoard(self):
        print("1 2 3 4 5 6 7")
        for row in self.currentBoard:
            for col in row:
                print(col, end=" ")
            print("\n")

    def updateBoard(self, col, playermark):
        valid=False
        while not valid:
            try:
                col=int(col)
                col-=1
                if col>=0 and col<=6:
                    valid=True
            except:
                print("please inpiut a number between 1-7 ")
                col=input("")
        
        for i,row in enumerate(self.currentBoard):
            if row[col]==".":
                if i==5:
                    self.currentBoard[i][col]=playermark 
                else:   
                    continue
            else:
                self.currentBoard[i-1][col]=playermark
    

    def checkWin(self, playermark):
        rowIndex=5
        # were checking bottom up(if there is a column win)
        for colIndex in range(7):
            for rowIndex in range(3):
                if self.currentBoard[5-rowIndex][colIndex]==playermark:
                    if self.currentBoard[5-rowIndex-1][colIndex]==playermark:
                        if self.currentBoard[5-rowIndex-2][colIndex]==playermark:
                            if self.currentBoard[5-rowIndex-3][colIndex]==playermark:
                                return True
        # were checking a left to right row win going from top to bottom 
        for rowIndex in range(6):
            for colIndex in range(4):
                if self.currentBoard[rowIndex][colIndex]==playermark:
                    if self.currentBoard[rowIndex][colIndex+1]==playermark:
                        if self.currentBoard[rowIndex][colIndex+2]==playermark:
                            if self.currentBoard[rowIndex][colIndex+3]==playermark:
                                return True
        # were checking for diaganols starting top left and going to the bottom right
        for rowIndex in range(3):                    
            for colIndex in range(4):                            
                if self.currentBoard[rowIndex][colIndex]==playermark:
                    if self.currentBoard[rowIndex+1][colIndex+1]==playermark:
                        if self.currentBoard[rowIndex+2][colIndex+2]==playermark:
                            if self.currentBoard[rowIndex+3][colIndex+3]==playermark:
                                return True

        for rowIndex in range(3):
            colIndex=6                    
            while colIndex>2:                            
                if self.currentBoard[rowIndex][colIndex]==playermark:
                    if self.currentBoard[rowIndex+1][colIndex-1]==playermark:
                        if self.currentBoard[rowIndex+2][colIndex-2]==playermark:
                            if self.currentBoard[rowIndex+3][colIndex-3]==playermark:
                                return True
                colIndex-=1
    
    def save(self, currentBoard, player1, player2, turn):
        saved=[]
        time=datetime.now().time()
        saved.append(currentBoard)
        saved.append(player1)
        saved.append(player2)
        saved.append(turn)
        dict={
            saved:time
        }
        return dict 