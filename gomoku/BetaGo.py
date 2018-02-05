import time
import os
import numpy as np

# The player's name
team_name = "BetaGo"

# List for converting between 0 indexed matrix indices and the lettered columns of the board
a2i = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

# board dimensions
board_height = 15
board_width = 15

# locally stored game state
globalboard = np.zeros((board_height,board_width))

# Keeps track of game state
playing = True
firstMove = True # is it currently the first move
swapTurn = False # is it currently the second turn where swaps are allowed


# Begin playing the game
def init():

    # while game is active
    while(True):
        # wait for the player's turn
        waitForTurn()
        if(playing):
            # choose a move
            chooseMove()
            #os.remove(team_name + ".go")
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

# marks a move by either player on the locally stored board
def storeMove(isme, i, j):
    global firstMove
    global swapTurn
    if(swapTurn):
        swapTurn = False
    if(firstMove):
        firstMove = False
        swapTurn = True
    if(isme):
        globalboard[i,j] = 1
    else:
        globalboard[i,j] = -1

# waits for the player's turn
def waitForTurn():
    # while the game is active
    while(True):
        # Look for the .go file for the player
        if(os.path.isfile(team_name + ".go")):
            # Check if the end_game file is present
            if(os.path.isfile("end_game")):
                # shut down because the game is over
                print team_name + " shutting down"
                playing = False
                exit(1)
            # If the game hasnt ended, read the contents of move_file
            with open("move_file") as moveFile:
                # read the first line and split it into its parts
                line = moveFile.readline()
                parts = line.split()

                if len(parts) > 0:
                    player= parts[0]
                    col = parts[1]
                    row = parts[2]
                    # convert board indices to matrix indices
                    i, j = board2matrixCoords(col, row)
                    # store the move locally
                    storeMove(False, i, j)
                return
        # wait another tenth of a second before checking again
        time.sleep(0.1)

# Makes a move for the player
# stores that move locally and also writes the move to move_file
def makeMove(i,j):
    # store move locally
    storeMove(True, i,j)
    # convert matrix indices to board indices
    boardMove = matrix2boardCoords(i,j)
    # build move string
    moveStr = team_name+ " " + boardMove[0] + " " + boardMove[1]

    # write move string to move_file
    with open("move_file", 'w') as moveFile:
        moveFile.write(moveStr)
    return

# Decide on a move to make and make that move
def chooseMove():
    # find a move through miniMaxDecision
    move = miniMaxDecision(globalboard)
    # make the move
    makeMove(move[0], move[1])


# helper function for getScore
# increments counts and scores, as well as updating the prev variable
# INPUT - val - value of the tile being looked at (-1 = enemy, 0 = empty, 1 = player)
# INPUT - prev - a record of whether or not the current block of "in a row" tiles had an empty tile before it
#       (2 = yes, -2 = no)
# INPUT - mycount - current count of "in a row" tiles for player
# INPUT - theircount - current count of "in a row" tiles for the enemy
# INPUT - score - current score of the board
# OUTPUT - all the same variables (except val) with an additional win variable, which is 1 if player won, -1 if enemy won, and 0 if nobody won
def checkCount(val, prev, mycount, theircount, score):
    # if current tile has the player's tile
    if(val == 1):
        # If this is the end of an enemy "in a row"
        if(theircount > 0):
            # if it began with an empty space, one empty is present, give negative "in a row" squared points
            if(prev == 2):
                score -= theircount*theircount
                # prev is now a "no"
                prev = -2
            # if it did not begin with an empty space, neither side of this "in a row" is unblocked, so simply assign negative "in a row" pounts
            else:
                score -= theircount
            # reset theircount
            theircount = 0
        # increment mycount
        mycount += 1
        # check if player won
        if(mycount >= 5):
            # return an exremely large score
            return 1,0,0,999999999, 1

    # If the tile has the enemy's peice on it
    elif(val == -1):
        # If this is the end of a player's "in a row"
        if(mycount > 0):
            # If the beginning of the player's "in a row" was unblocked, give "in a row" squared points
            if(prev == 2):
                score += mycount*mycount
                # reset prev to "no"
                prev = -2
            # if the beginning of the player's "in a row" was blocked, then both sides are blocked. Simply give "in a row" points
            else:
                score += mycount
            # reset mycount
            mycount = 0
        # increment theircount
        theircount += 1
        # check if the enemy won
        if(theircount >= 5):
            # return an extremely low score
            return -1,0,0,-999999999, -1
        
    # if the tile is empty or the end of the board
    else:
        # If this ends an enemy "in a row"
        if(theircount > 0):
            # If this is an empty square, there is at least one unblocked space next to the "in a row"
            if(val == 0):
                # if prev = 2, both sides of the "in a row" are unblocked, award negative "in a row" cubed points
                if(prev == 2):
                    score -= theircount * theircount * theircount
                # Otherwise, this "in a row" is only unlocked on one side, award negative "in a row" squared points
                else:
                    score-= theircount * theircount
            # Reset theircount
            theircount = 0
        # If this ends a player's "in a row"        
        if(mycount > 0):
            # If this is an empty tile, there is at least one unblocked space next to the "in a row"
            if(val == 0):
                # if prev = 2, both sides of the "in a row" are unblocked, award "in a row" cubed points
                if(prev == 2):
                    score += mycount * mycount * mycount
                # Otherwise, this "in a row" is only unlocked on one side, award "in a row" squared points
                else:
                    score += mycount * mycount
            # Reset mycount
            mycount = 0
        # If the tile was empty, set prev to 2 indicating a following "in a row" is unblocked on the leading end
        if(val == 0):
            prev = 2

    # return all inputs except val
    return prev, mycount, theircount, score, 0

# Gets an evaluation score of a board configuration
# INPUT - board - a numpy matrix representing the board configuration
# OUTPUT - score - the evaluation score of the board, an integer
# OUTPUT - win - 1 if the player won, -1 if the enemy won, and 0 if nobody won
def getScore(board):
    score = 0 # total of the score to return
    mycount = 0 # counts number of player tiles in a row
    theircount = 0 # counts number of enemy tiles in a row
    win = 0 # looks for the end of a game
    prev = -2 # records presence of open tiles
    
    # Looks across each row of the board for horizontal "in a rows"
    for i in range(board_height):
        # reset counts for each row
        mycount = 0
        theircount = 0
        prev = -2
        # go through each row looking for "in a rows"
        for j in range(board_width):
            square = board[i,j]
            prev, mycount, theircount, score, win = checkCount(square, prev, mycount, theircount, score)
            # returns if 5 in a row is found
            if(win != 0):
                return score, win
        # runs one more time at the board's edge
        prev, mycount, theircount, score, win = checkCount(-2, prev, mycount, theircount, score)
        # returns if 5 in a row is found
        if(win != 0):
            return score, win

    # Each of the falling code chunks in getScore are the same as the previously, just checking different directions

    
    # Looks across each column for "in a rows"
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

        
    # Looks at the lower left side of the board for diagonal "in a rows"
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

    # Looks across the upper right side of the board for diagonal "in a rows"
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

    # Looks across the upper left side of the board for diagonal "in a rows"
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

    # Looks across the lower right side of the board for diagonal "in a rows"
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
        
    # return the score
    return score, 0


# base number of best board configurations to check
k = 300


# Uses mini-max with alpha-beta pruning, iterative deepening, and K-best methods to make a decision about what the best move is for player
# INPUT - board - the current board configuration
# OUTPUT - a tuple containing the i and j indices in matrix indices of the move decided on to make
def miniMaxDecision(board):
    # Save the time at which a move must be made, with a second of leeway for finishing up and writing the move
    timeup = time.time() + 9.0
    # Start the maximum depth at 1 for iterative deepening
    maxDepth = 1
    # store the default best move as the middle of the board, which is only returned in case of errors
    bestmove = [board_height/2, board_width/2, 4]

    # run until time is up
    while(time.time() < timeup):
        # use a copy of the board so as to not edit the local copy
        b = np.copy(board)

        # find the best move looking up to maxDepth
        v, move = maxValue(b, float('-inf'), float('inf'), 0, maxDepth, timeup)

        # If time ran out in the middle of looking at this depth, use the most recently completed depth's move instead
        # This was done because incomplete depths would miss winning or losing moves. I believe there is a way to use the incomplete
        # depths but I was unable to discover and correctly implement one
        if(time.time() > timeup):
            return bestmove[0], bestmove[1]

        # Make sure the move is on the board, return the last valid move if an error occurred
        if(move[0] < 0 or move[0] >= board_height or move[1] < 0 or move[1] >= board_width):
            return bestmove[0], bestmove[1]

        # save the new best move
        bestmove = [move[0], move[1], v]
        # if a win is found, stop searching and play that win!!
        if(bestmove[2] > 99999999):
            return bestmove[0], bestmove[1]

        # increase max depth by 2. This was initially done so
        maxDepth += 2

    return bestmove[0], bestmove[1]


# Makes a maximization decision in minimax
# INPUT - board - the board configuration of the current node
# INPUT - alpha - the alpha value used in alpha-beta pruning
# INPUT - beta  - the beta value used in alpha-beta pruning
# INPUT - depth - current depth of the node
# INPUT - maxDepth - current depth limit
# INPUT - timeup - time at which calculation must stop
# OUTPUT - v - the predicted score of the move
# OUTPUT - move - a tuple representing (i,j) the matrix indices of the latest move made to reach the node's board configuration
def maxValue(board, alpha, beta, depth, maxDepth, timeup):
    # initalize move and v
    move = [-1, -1]
    # start v as the lowest value possible
    v = float('-inf')

    # create a queue of nodes to expand
    queue = []

    # Ending criteria, if maxDepth reached, return empty values. The correct values are set in the calling function
    if(depth >= maxDepth):
        return 0, move

    # If this is the first move, consider only 3 moves in order to trim the tree as small as possible
    # The 3 moves considered are one at the corner of the board, one on the edge of the board, and one in the middle of the board
    if(firstMove and depth == 0):
        # add the middle move to the queue
        i = board_height/2
        j = board_width/2
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMaxSuccessor(queue, i, j, score, depth)

        # add the edge move to the queue
        i = 0
        j = 10
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMaxSuccessor(queue, i, j, score, depth)

        # add the corner move to the queue
        i = 0
        j = 0
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMaxSuccessor(queue, i, j, score, depth)

    # If the current turn is the second turn and a swap is an option, consider only three moves in order to trim the tree as much as possible
    # Three moves considered are the swapping move, and 2 moves far enough away from each other that at least one is garunteed to be seperate from the enemy
    if(swapTurn and depth == 0):
        i, j = findFirstMove(board)
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMaxSuccessor(queue, i, j, score, depth)

        i = 4
        j = 7
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMaxSuccessor(queue, i, j, score, depth)

        i = 10
        j = 4
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMaxSuccessor(queue, i, j, score, depth)

    # If neither the first or second turn, simply consider all moves on spaces adjacent to tiles that are filled
    # We did this in order to only consider the plays likely to be important, which are blocking and attacking moves
    else:
        # Go through each tile
        for i in range(board_height):
            for j in range(board_width):
                # If the tile is bordering(includes diagonals) a non-empty tile, consider it
                if(board[i, j] == 0 and checkBordering(board, i, j)):
                    # Create board configuration where this move is made
                    b = np.copy(board)
                    b[i, j] = 1 # make move for player
                    # Evaluate this board
                    score, win = getScore(b)
                    # If the board is a winning board, end this branch and return this move with a high score
                    if(win == 1):
                        return 999999999, [i, j]
                    # Add the move and score to a highest-score-first queue
                    addMaxSuccessor(queue, i, j, score, depth)
    # If time is up, return best estimated child move
    if(time.time() >= timeup):
        if(len(queue) > 0):
            return queue[0][2], [queue[0][0],queue[0][1]]

    # Go through queue and check the k/depth best child nodes
    for s in queue:
        # If time up, return best move so far
        if(time.time() >= timeup):
            return v, move
        # rebuild the board with current move
        b = np.copy(board)
        i = s[0]
        j = s[1]
        # get the boards score
        score = s[2]
        b[i, j] = 1
        
        # Expand the children min nodes with depth as 1 deeper
        minTurn = minValue(b, alpha, beta, depth+1, maxDepth, timeup)

        # If the minturn returns invalid moves, the terminal depth was reached. Use the known score and move
        # If the known score is better than the current best, save the score and move
        if(minTurn[1][0] < 0 and score > v):
            move = [i,j]
            v = score
        # Otherwise, get the score of the minimized children nodes, and save it as the best if it exceeds the current best score
        elif minTurn[0] > v:
            move = [i,j]
            v = minTurn[0]
        # if the best score exceeds beta, prune this branch
        if(v >= beta):
            return v, [i,j]
        # update alpha if the best score exceeds alpha
        alpha = max(alpha, v)
    return v, move

# same as maxValue except for a min player (the enemy) move (see comments from maxValue
def minValue(board, alpha, beta, depth, maxDepth, timeup):
    move = [-1, -1]
    v = float('inf')
    queue = []
    if(depth >= maxDepth):
        return 0, move

    if(firstMove and depth == 1):
        i, j = findFirstMove(board)
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMinSuccessor(queue, i, j, score, depth)

        i = 4
        j = 7
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMinSuccessor(queue, i, j, score, depth)

        i = 10
        j = 4
        b = np.copy(board)
        b[i, j] = 1
        score, win = getScore(b)
        addMinSuccessor(queue, i, j, score, depth)
    else:
        for i in range(board_height):
            for j in range(board_width):
                if(board[i, j] == 0 and checkBordering(board, i, j)):
                    b = np.copy(board)
                    b[i, j] = -1
                    score, win = getScore(b)
                    if(win == -1):
                        return -999999999, [i, j]
                    addMinSuccessor(queue, i, j, score, depth)

    if(time.time() >= timeup):
        if(len(queue) > 0):
            return queue[0][2], [queue[0][0],queue[0][1]]
    for s in queue:
        if(time.time() >= timeup):
            return v, move
        b = np.copy(board)
        i = s[0]
        j = s[1]
        score = s[2]
        b[i, j] = -1
        maxTurn = maxValue(b, alpha, beta, depth+1, maxDepth, timeup)
        if(maxTurn[1][0] < 0 and score < v):
            move = [i,j]
            v = score
        elif maxTurn[0] < v:
            move = [i,j]
            v = maxTurn[0]
        if(v <= alpha):
            return v, [i,j]
        beta = min(beta, v)
    return v, move

# Adds a move and its score to a queue
# The queue is a highest-score-first queue and is kept to k/depth length
# INPUT - queue - queue to alter
# INPUT - i - row index of the move
# INPUT - j - column index of the move
# INPUT - score - score of the board configuration with the move present
# INPUT - depth - the current depth of the node using this given queue
def addMaxSuccessor(queue, i, j, score, depth):

    # goes through queue until the appropriate spot is found
    for n in range(len(queue)):
        if(score >= queue[n][2]):
            queue.insert(n, [i, j, score])
            # If queue length exceeds k/(depth+1), trim the end
            while(len(queue) > k/(depth + 1)):
                queue.pop()
            return
    # Add to the end if the score is less than all current entries
    queue.append([i, j, score])
    # Trim again if queue exceeds limit
    while(len(queue) > k/(depth + 1)):
        queue.pop()

# Adds a move and its score to a queue
# The queue is a lowest-score-first queue and is kept to k/depth length
# INPUT - queue - queue to alter
# INPUT - i - row index of the move
# INPUT - j - column index of the move
# INPUT - score - score of the board configuration with the move present
# INPUT - depth - the current depth of the node using this given queue
def addMinSuccessor(queue, i, j, score, depth):
    # goes through queue until the appropriate spot is found
    for n in range(len(queue)):
        if(score <= queue[n][2]):
            queue.insert(n, [i, j, score])
            # If queue length exceeds k/(depth+1), trim the end
            while(len(queue) > k/(depth + 1)):
                queue.pop()
            return
    # Add to the end if the score is more than all current entries
    queue.append([i, j, score])
    # Trim again if queue exceeds limit
    while(len(queue) > k/(depth + 1)):
        queue.pop()


# checks if the coordinates given on the board is next to (including diagonals) a tile with a player on it
# INPUT - board - board configuration being checked
# INPUT - i - row index of the move
# INPUT - j - column index of the move
# OUTPUT - true if next to a player's tile, false otherwise
def checkBordering(board, i, j):
    # start as false
    border = False

    # variables holding the contraints of the search. Start at given move and expand outwards if not on the edges of the board
    minx = j
    maxx = j
    miny = i
    maxy = i

    # Checks each direction to see if on the edge of the board. Expands outwards if possible
    if(j-1 >= 0):
        minx = j-1
    if(j+1 < board_width):
        maxx = j+1
    if(i-1 >= 0):
        miny = i-1
    if(i+1 < board_height):
        maxy = i+1

    # Search around the move for non-zero board entries (indicating non-empty)
    for n in range(miny, maxy+1):
        for m in range(minx, maxx+1):
            # become true if a player peice is found
            border = border or (board[n,m] != 0)

    return border

# Searches the board for the "first move" which would be the only move present
# INPUT - board - board to search
# OUTPUT - a tuple representing the indices of the move's location
def findFirstMove(board):

    # search the board for a nonzero entry and immediately return its location when found
    for i in range(board_height):
        for j in range(board_width):
            if(board[i,j] != 0):
                return i,j
    return board_height/2, board_width/2

    
init()

