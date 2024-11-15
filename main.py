import board
import datetime
import json
import os

def get_files(path):
    """Gets all files in the specified directory."""
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            files.append(os.path.join(path,entry))
    return files

def setup():
    files=[]
    if not os.path.isdir("savedgames"):
        os.mkdir("savedgames")
    else:
        files=get_files("savedgames")
    return files

def save(gameboard, player1, player2, turn):

    time=datetime.datetime.now()
    time = time.strftime("%I-%M %p on %A %B %d %Y")
    time=time.split(".")[0]
    filename=f"{player1}-{player2}-{time}"
    saveData={
        "time":time,
        "board":gameboard.currentBoard,
        "player1 name":player1,
        "player2 name":player2,
        "current turn":turn
    }
    json_data=json.dumps(saveData)
    filepath=os.path.join("savedgames", filename)
    with open(f"{filepath}.txt", "w") as f:
        f.write(json_data)
    
def load(savedgames):
    isint=False
    for i,game in enumerate(savedgames):
        print(f"{i+1}) {game}")
    while not isint:
        gameload=input("Which game do you want to load (specify with the index): \n")
        try:
            gameload=int(gameload)
            datapath=savedgames[gameload-1]
            isint=True
        except:
            print(f"please chose a valid number between 1-{len(savedgames)}" )
        
    with open(f"{datapath}","r") as f:
        savedata=f.read()
    savedata=json.loads(savedata)
    return savedata

def gamesetup(player1, player2, turn=None, newboard=None):
    names={}
    names[player1]="x"
    names[player2]="o"
    if newboard:
        gameboard=board.Board(newboard)
    else:    
        gameboard=board.Board()
    gameboard.printBoard()
    if not turn:
        turn=player1
    return (names, gameboard, turn)

def nextTurn(player1, player2, gameboard, turn, names):
    play=input(f"{turn} where would you like to place your piece? (type s to save) \n")
    if play=="s":
        save(gameboard, player1, player2, turn)
    gameboard.updateBoard(play, names[turn])
    gameboard.printBoard()
    win=gameboard.checkWin(names[turn])
    if turn==player1:
        turn=player2
    else:
        turn=player1
    return win, turn

def handleMenu():
    savefiles=setup()
    print("Welcome to Four-in-a-row!")
    print("Please choose an option from the following menu:")
    print("1) Start new game")
    print("2) Load game")
    print("3) Quit")
    selection=input("")
    if selection=="1":

        player1=input("Player 1 - What is your name? \n ")
        player1=player1.capitalize()
        player2=input("Player 2 - What is your name? \n ")
        player2=player2.capitalize()
        names,gameboard,turn=gamesetup(player1, player2)
        win=False

        while not win:
            win,turn=nextTurn(player1, player2, gameboard, turn, names)
            
    elif selection=="2":
        data=load(savefiles)
        names,gameboard,turn=gamesetup(data["player1 name"], data["player2 name"], data["current turn"], data["board"])
        player1=data["player1 name"]
        player2=data["player2 name"]
        win=False

        while not win:
            win,turn=nextTurn(player1, player2, gameboard, turn, names)
    elif selection=="3":
        exit()
    else:
        print("Please choose an option from the menu")
        handleMenu()
        

handleMenu()


