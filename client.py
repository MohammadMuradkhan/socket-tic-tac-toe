import socket
import pickle
from colorama import Fore, Style, init

init(autoreset=True)

SERVER_IP = "10.25.197.61"
PORT = 5050

def colorize(cell):
    if cell == "X":
        return Fore.RED + "X" + Style.RESET_ALL
    elif cell == "O":
        return Fore.BLUE + "O" + Style.RESET_ALL
    return " "

def print_board(b):
    print(Fore.YELLOW + "\n   TIC TAC TOE (You = O)\n")
    print(f"   {colorize(b[0])} | {colorize(b[1])} | {colorize(b[2])}")
    print("  ---+---+---")
    print(f"   {colorize(b[3])} | {colorize(b[4])} | {colorize(b[5])}")
    print("  ---+---+---")
    print(f"   {colorize(b[6])} | {colorize(b[7])} | {colorize(b[8])}\n")

def check_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,c,d in wins:
        if b[a] == b[c] == b[d] != " ":
            return b[a]
    if " " not in b:
        return "Draw"
    return None

sock = socket.socket()
sock.connect((SERVER_IP, PORT))
print(Fore.CYAN + "[CLIENT] Connected to server.")

while True:
    board, winner = pickle.loads(sock.recv(1024))
    print_board(board)

    if winner:
        print(Fore.MAGENTA + "Result:", winner)
        break

    try:
        move = int(input(Fore.GREEN + "Your move (0-8): "))
    except:
        continue

    if move < 0 or move > 8 or board[move] != " ":
        print(Fore.RED + "Invalid move!")
        continue

    board[move] = "O"
    winner = check_winner(board)

    sock.send(pickle.dumps((board, winner)))
