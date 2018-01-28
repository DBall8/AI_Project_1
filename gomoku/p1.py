import time
import os
import numpy as np

team_name = "p1"

a2i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

board_height = 15
board_width = 15
board = np.zeros((board_height,board_width))

playing = True

def init():
    while(True):
        waitForTurn()
        if(playing):
            chooseMove()
            os.remove(team_name + ".go")
        else:
            return

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
            if(os.path.isfile("end_game")):
                print team_name + " shutting down"
                exit(1)
            with open("move_file") as moveFile:
                line = moveFile.readline()
                parts = line.split()
                if len(parts) > 0:
                    player= parts[0]
                    col = parts[1]
                    row = parts[2]
                    i, j = board2matrixCoords(col, row)
                    storeMove(False, i, j)
                return
        time.sleep(0.1)

def makeMove(i,j):
    storeMove(True, i,j)
    boardMove = matrix2boardCoords(i,j)
    moveStr = team_name+ " " + boardMove[0] + " " + boardMove[1]
    with open("move_file", 'w') as moveFile:
        moveFile.write(moveStr)
    return

def chooseMove():
    for i in range(15):
        for j in range(15):
            if(board[i,j] == 0):
                makeMove(i,j)
                return

# helper function for getScore
def checkCount(val, mycount, theircount, score):
    if(val == 1):
        mycount += 1
        if(theircount != 0):
            score -= theircount * theircount
            theircount = 0
    elif(val == -1):
        theircount += 1
        if(mycount != 0):
            score += mycount * mycount
            mycount = 0
    else:
        if(theircount != 0):
            score -= theircount * theircount
            theircount = 0
        if(mycount != 0):
            score += mycount * mycount
            mycount = 0
    return mycount, theircount, score

# gets an evaluation score of a board configuration
def getScore(board):
    score = 0
    mycount = 0
    theircount = 0

    # counts horizontally
    for i in range(board_height):
        mycount = 0
        theircount = 0
        for j in range(board_width):
            square = board[i,j]
            mycount, theircount, score = checkCount(square, mycount, theircount, score)
        mycount, theircount, score =  checkCount(0, mycount, theircount, score)

    # counts vertically
    for j in range(board_width):
        mycount = 0
        theircount = 0
        for i in range(board_height):
            square = board[i,j]
            mycount, theircount, score = checkCount(square, mycount, theircount, score)
        mycount, theircount, score =  checkCount(0, mycount, theircount, score)

    # counts lower left triangle
    for i in range(board_height):
        mycount = 0
        theircount = 0
        for j in range(board_width-i):
            square = board[i+j,j]
            mycount, theircount, score = checkCount(square, mycount, theircount, score)
        mycount, theircount, score =  checkCount(0, mycount, theircount, score)
        
    # counts upper right triangle
    for i in range(1, board_height):
        mycount = 0
        theircount = 0
        for j in range(board_height-i):
            square = board[j,i+j]
            mycount, theircount, score =  checkCount(square, mycount, theircount, score)
        mycount, theircount, score =  checkCount(0, mycount, theircount, score)

    #counts upper left triangle
    for i in range(board_height):
        mycount = 0
        theircount = 0
        for j in range(i+1):
            square = board[i-j,j]
            mycount, theircount, score =  checkCount(square, mycount, theircount, score)
        mycount, theircount, score =  checkCount(0, mycount, theircount, score)

    #counts lower right triangle
    for i in range(board_width-1):
        mycount = 0
        theircount = 0
        for j in range(board_width-1, i, -1):
            square = board[j, board_height-j+i]
            mycount, theircount, score =  checkCount(square, mycount, theircount, score)
        mycount, theircount, score =  checkCount(0, mycount, theircount, score)
            
    return score

maxDepth = 1

def miniMaxDecision(board):
    v = maxValue(board)

def maxValue(board):

def minValue(board):
    
init()

