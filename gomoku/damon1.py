import time
import os
import numpy as np

team_name = "p1"

a2i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

board_height = 15
board_width = 15
globalboard = np.zeros((board_height,board_width))

playing = True

def init():
##    globalboard[5,3] = -1
##    globalboard[5,4] = -1
##    #print getScore(globalboard)
##    globalboard[6,4] = 1
##    #print globalboard
##    #print maxValue(globalboard, float('-inf'), float('inf'), 0, 1, time.time() + 9)
##    globalboard[7,5] = 1
##    print globalboard
##    print getScore(globalboard)
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
        globalboard[i,j] = 1
    else:
        globalboard[i,j] = -1

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
    move = miniMaxDecision(globalboard)
    makeMove(move[0], move[1])

# helper function for getScore
def checkCount(val, prev, mycount, theircount, score):
    if(val == 1):
        if(theircount > 0):
            if(prev == 2):
                score -= theircount
                prev = -2
            score -= theircount * theircount * theircount
            theircount = 0
        mycount += 1
        if(mycount >= 5):
            return 1,0,0,999999999, 1
    elif(val == -1):
        if(mycount > 0):
            if(prev == 2):
                score += mycount
                prev = -2
            score += mycount * mycount * mycount
            mycount = 0
        theircount += 1
        if(theircount >= 5):
            return -1,0,0,-999999999, -1
    else:
        if(theircount > 0):
            if(val == 0):
                score-= theircount
            if(prev == 2):
                score -= theircount
            score -= theircount * theircount * theircount
            theircount = 0
        if(mycount > 0):
            if(val == 0):
                score += mycount
            if(prev == 2):
                score += mycount
            score += mycount * mycount * mycount
            mycount = 0
        if(val == 0):
            prev = 2
        
    return prev, mycount, theircount, score, 0

# gets an evaluation score of a board configuration
def getScore(board):
    score = 0
    mycount = 0
    theircount = 0
    win = 0
    prev = -2

    #prevscore = 0
    
    # counts horizontally
    for i in range(board_height):
        mycount = 0
        theircount = 0
        prev = -2
        for j in range(board_width):
            square = board[i,j]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            if(win != 0):
                return score, win
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        if(win != 0):
            return score, win
        
    #print "HORIZONTAL " + str(score-prevscore)
    #prevscore = score
    
    # counts vertically
    for j in range(board_width):
        mycount = 0
        theircount = 0
        prev = -2
        for i in range(board_height):
            square = board[i,j]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            if(win != 0):
                return score, win
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        if(win != 0):
            return score, win
        
    #print "VERTICAL " + str(score-prevscore)
    #prevscore = score
    
    # counts lower left triangle
    for i in range(board_height):
        mycount = 0
        theircount = 0
        prev = -2
        for j in range(board_width-i):
            square = board[i+j,j]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            if(win != 0):
                return score, win
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        if(win != 0):
            return score, win

    #print "LOWER LEFT " + str(score-prevscore)
    #prevscore = score
    
    # counts upper right triangle
    for i in range(1, board_height):
        mycount = 0
        theircount = 0
        prev = -2
        for j in range(board_height-i):
            square = board[j,i+j]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            if(win != 0):
                return score, win
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        if(win != 0):
            return score, win

    #print "UPPER RIGHT " + str(score-prevscore)
    #prevscore = score

    #counts upper left triangle
    for i in range(board_height):
        mycount = 0
        theircount = 0
        prev = -2
        for j in range(i+1):
            square = board[i-j,j]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            if(win != 0):
                return score, win
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        if(win != 0):
            return score, win

    #print "UPPER LEFT " + str(score-prevscore)
    #prevscore = score

    #counts lower right triangle
    for i in range(board_width-1):
        mycount = 0
        theircount = 0
        prev = -2
        for j in range(board_width-1, i, -1):
            square = board[j, board_height-j+i]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            if(win != 0):
                return score, win
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        if(win != 0):
            return score, win
        
    #print "LOWER RIGHT " + str(score-prevscore)
    #prevscore = score
            
    return score, 0


k = 100

def miniMaxDecision(board):
    timeup = time.time() + 9.0
    maxDepth = 1
    bestmove = [board_height/2, board_width/2, 4]
    while(time.time() < timeup):
        b = np.copy(board)
        v = maxValue(b, float('-inf'), float('inf'), 0, maxDepth, timeup)
        if(time.time() > timeup):
            return bestmove[0], bestmove[1]
        move = v[1]
        if(move[0] < 0 or move[0] >= board_height or move[1] < 0 or move[1] >= board_width):
            return bestmove
        bestmove = [move[0], move[1], v[0]]
        if(bestmove[2] > 99999999):
            return bestmove[0], bestmove[1]
        maxDepth += 1
        
    return bestmove[0], bestmove[1]

def maxValue(board, alpha, beta, depth, maxDepth, timeup):
    move = [-1, -1]
    v = float('-inf')
    queue = []
    if(depth >= maxDepth):
        print depth
        score, win = getScore(board)
        return score, move
    for i in range(board_height):
        for j in range(board_width):
            if(board[i, j] == 0 and checkBordering(board, i, j)):
                b = np.copy(board)
                b[i, j] = 1
                score, win = getScore(board)
                if(win == 1):
                    return 999999999, [i, j]
                addMaxSuccessor(queue, i, j, score)

    for s in queue:
        if(time.time() >= timeup):
            return queue[2], [queue[0],queue[1]]
        b = np.copy(board)
        i = s[0]
        j = s[1]
        b[i, j] = 1
        minTurn = minValue(b, alpha, beta, depth+1, maxDepth, timeup)
        if minTurn[0] > v:
            move = [i,j]
            v = minTurn[0]
        if(v >= beta):
            return v, [i,j]
        alpha = max(alpha, v)
    return v, move

def minValue(board, alpha, beta, depth, maxDepth, timeup):
    move = [-1, -1]
    v = float('inf')
    queue = []
    if(depth >= maxDepth):
        print depth
        score, win = getScore(board)
        return score, move
    for i in range(board_height):
        for j in range(board_width):
            if(board[i, j] == 0 and checkBordering(board, i, j)):
                b = np.copy(board)
                b[i, j] = -1
                score, win = getScore(board)
                if(win == -1):
                    return -999999999, [i, j]
                addMinSuccessor(queue, i, j, score)

    for s in queue:
        if(time.time() >= timeup):
            return queue[2], [queue[0],queue[1]]
        b = np.copy(board)
        i = s[0]
        j = s[1]
        b[i, j] = -1
        maxTurn = maxValue(b, alpha, beta, depth+1, maxDepth, timeup)
        if maxTurn[0] < v:
            move = [i,j]
            v = maxTurn[0]
        if(v <= alpha):
            return v, [i,j]
        beta = min(beta, v)
    return v, move

def addMaxSuccessor(queue, i, j, score):
    for n in range(len(queue)):
        if(score >= queue[n][2]):
            queue.insert(n, [i, j, score])
            while(len(queue) > k):
                queue.pop()
            return
    queue.append([i, j, score])
    while(len(queue) > k):
        queue.pop()

def addMinSuccessor(queue, i, j, score):
    for n in range(len(queue)):
        if(score <= queue[n][2]):
            queue.insert(n, [i, j, score])
            while(len(queue) > k):
                queue.pop()
            return
    queue.append([i, j, score])
    while(len(queue) > k):
        queue.pop()


def checkBordering(board, i, j):
    border = False
    minx = j
    maxx = j
    miny = i
    maxy = i
    
    if(j-1 >= 0):
        minx = j-1
    if(j+1 < board_width):
        maxx = j+1
    if(i-1 >= 0):
        miny = i-1
    if(i+1 < board_height):
        maxy = i+1

    for n in range(miny, maxy+1):
        for m in range(minx, maxx+1):
            border = border or (board[n,m] != 0)

    return border

    
init()

