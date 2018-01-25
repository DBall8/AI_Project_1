import time
import os
import numpy as np


team_name = "p2"

a2i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
board = np.zeros((15,15))

def init():
    while(True):
        waitForTurn()
        chooseMove()
        os.remove(team_name + ".go")

# Converts board coordinates into matrix coordinates
def board2matrixCoords(col, row):
    i = int(row) - 1
    j = a2i.index(col.upper())
    return i,j
# converts matrix coordinates to board coordinate
def matrix2boardCoords(i, j):
    col = a2i[j]
    row = str(i+1)
    return col,row

# marks a move by either player on the local board
def storeMove(isme, i, j):
    if(isme):
        board[i,j] = 1
    else:
        board[i,j] = -1

def waitForTurn():
    while(True):
        if(os.path.isfile(team_name + ".go")):
            print "HI"
            with open("move_file") as moveFile:
                line = moveFile.readline()
                parts = line.split()
                if len(parts) > 0:
                    print team_name + " Found the file"
                    player= parts[0]
                    col = parts[1]
                    row = parts[2]
                    i, j = board2matrixCoords(col, row)
                    storeMove(False, i, j)
                return
        time.sleep(0.1)

def makeMove(i,j):
    print team_name + " making move"
    storeMove(True, i,j)
    boardMove = matrix2boardCoords(i,j)
    moveStr = team_name+ " " + boardMove[0] + " " + boardMove[1]
    with open("move_file", 'w') as moveFile:
        moveFile.write(moveStr)
    return

def chooseMove():
    print team_name + " Choosing move"
    for i in range(15):
        for j in range(15):
            if(board[i,j] == 0):
                makeMove(i,j)
                return
                
        
init()
