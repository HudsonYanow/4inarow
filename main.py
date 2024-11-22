import board
import datetime
import json
import os

def get_files(path):
    """
    Retrieves a list of all file paths in the specified directory.

    Args:
        path (str): The directory path where to search for files.

    Returns:
        list: A list of full file paths found in the directory.
    """
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            files.append(os.path.join(path, entry))
    return files

def setup():
    """
    Sets up the saved games directory and retrieves any existing saved games.

    Returns:
        list: A list of saved game file paths if they exist, otherwise an empty list.
    """
    files = []
    if not os.path.isdir("savedgames"):
        os.mkdir("savedgames")
    else:
        files = get_files("savedgames")
    return files

def save(gameboard, player1, player2, turn):
    """
    Saves the current game state to a file in the 'savedgames' directory.

    Args:
        gameboard (object): The current gameboard object.
        player1 (str): The name of player 1.
        player2 (str): The name of player 2.
        turn (str): The name of the player whose turn it is.
    """
    time = datetime.datetime.now()
    time = time.strftime("%I-%M %p on %A %B %d %Y")
    time = time.split(".")[0]
    filename = f"{player1}-{player2}-{time}"
    saveData = {
        "time": time,
        "board": gameboard.currentBoard,
        "player1 name": player1,
        "player2 name": player2,
        "current turn": turn
    }
    json_data = json.dumps(saveData)
    filepath = os.path.join("savedgames", filename)
    with open(f"{filepath}.txt", "w") as f:
        f.write(json_data)

def load(savedgames):
    """
    Loads a previously saved game from a list of saved games.

    Args:
        savedgames (list): A list of saved game file paths.

    Returns:
        dict: The loaded game data in dictionary format.
    """
    isint = False
    for i, game in enumerate(savedgames):
        print(f"{i+1}) {game}")
    
    while not isint:
        gameload = input("Which game do you want to load (specify with the index): \n")
        try:
            gameload = int(gameload)
            datapath = savedgames[gameload - 1]
            isint = True
        except:
            print(f"Please choose a valid number between 1-{len(savedgames)}")
    
    with open(f"{datapath}", "r") as f:
        savedata = f.read()
    savedata = json.loads(savedata)
    return savedata

def gamesetup(player1, player2, turn=None, newboard=None):
    """
    Initializes the game state, including the player names, gameboard, and turn.

    Args:
        player1 (str): The name of player 1.
        player2 (str): The name of player 2.
        turn (str, optional): The player who should take the first turn. Defaults to None.
        newboard (object, optional): A new board state. Defaults to None.

    Returns:
        tuple: A tuple containing player names and symbols, gameboard object, and the first turn.
    """
    names = {}
    names[player1] = "x"
    names[player2] = "o"
    if newboard:
        gameboard = board.Board(newboard)
    else:
        gameboard = board.Board()
    gameboard.printBoard()
    if not turn:
        turn = player1
    return (names, gameboard, turn)

def nextTurn(player1, player2, gameboard, turn, names):
    """
    Handles the player's move, updates the gameboard, and checks for a win.

    Args:
        player1 (str): The name of player 1.
        player2 (str): The name of player 2.
        gameboard (object): The current gameboard object.
        turn (str): The player whose turn it is.
        names (dict): Dictionary mapping player names to their piece symbols.

    Returns:
        tuple: A tuple containing a boolean indicating whether the game has been won,
               and the updated turn (the other player's turn).
    """
    play = input(f"{turn} where would you like to place your piece? (type s to save) \n")
    if play == "s":
        save(gameboard, player1, player2, turn)
    gameboard.updateBoard(play, names[turn])
    gameboard.printBoard()
    win = gameboard.checkWin(names[turn])
    if turn == player1:
        turn = player2
    else:
        turn = player1
    return win, turn

def handleMenu():
    """
    Displays the main menu, handles user input for starting a new game, loading a game, or quitting.
    """
    savefiles = setup()
    print("Welcome to Four-in-a-row!")
    print("Please choose an option from the following menu:")
    print("1) Start new game")
    print("2) Load game")
    print("3) Quit")
    selection = input("")
    
    if selection == "1":
        player1 = input("Player 1 - What is your name? \n ")
        player1 = player1.capitalize()
        player2 = input("Player 2 - What is your name? \n ")
        player2 = player2.capitalize()
        names, gameboard, turn = gamesetup(player1, player2)
        win = False

        while not win:
            win, turn = nextTurn(player1, player2, gameboard, turn, names)
    
    elif selection == "2":
        data = load(savefiles)
        names, gameboard, turn = gamesetup(data["player1 name"], data["player2 name"], data["current turn"], data["board"])
        player1 = data["player1 name"]
        player2 = data["player2 name"]
        win = False

        while not win:
            win, turn = nextTurn(player1, player2, gameboard, turn, names)
    
    elif selection == "3":
        exit()
    else:
        print("Please choose an option from the menu")
        handleMenu()

# Start the game by calling the menu handler
handleMenu()


