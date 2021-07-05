"""
Tic Tac Toe Player
"""
import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Initialize counter for each player
    x_count = 0
    o_count = 0

    if terminal == True:
        return None

    # Iterated through every box in the board
    for i in board:
        for j in i:
            # Check box for X player's tile
            if j == X:
                # Add to X count
                x_count += 1
            # Check box for O player's tile
            if j == O:
                # Add to O count
                o_count += 1
    # Since X starts at the end of evey round there number of tiles of each player should be tied
    if x_count == o_count:
        return(X)
    # If the tile number are not equal then O has yet to play its move
    if x_count > o_count:
        return(O)

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Create empty list for actions
    actions = []
    # Itereate through the rows of the board
    for i in range(3):
        # Itereate through the cells of the rows
        for j in range(3):
            # If the cell is empty then this cells is a valid action
            if board[i][j] == EMPTY:
                # Apend the row and cell index to actions list
                temp = []
                temp.append(i)
                temp.append(j)
                actions.append(temp)
    # Return the actions list as a tuple
    return(tuple(actions))

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Slice the action into row and cell
    row = action[0]
    cell = action[1]
    # Make a deep copy of the game board such that we can mutate the copy without changing the actual board
    new_board = copy.deepcopy(board)
    # Check if action is allowed
    if new_board[row][cell] == EMPTY:
        # Check if whose play is it and fill in the selected cell with the respective tile
        if player(board) == X:
            new_board[row][cell] = X
            return (new_board)

        if player(board) == O:
            new_board[row][cell] = O
            return (new_board)
    #else:
        #raise NameError('Invalid Action')

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for 3 in a row in rows for X and O
    for i in board:
        x_count = i.count(X)
        o_count = i.count(O)
        if x_count == 3:
            return (X)
        if o_count == 3:
            return(O)
 

    # By transposing the board columns become rows and we can check for 3 in a row in the columns
    t_board = copy.deepcopy(board)
    t_board = np.transpose(t_board)

    # Check for 3 in a row for X and for O
    for i in t_board:
        x_count = 0
        o_count = 0
        for j in i:
            if j == X:
                x_count +=1
            if j == O:
                o_count +=1
        if x_count == 3:
            return(X)
        if o_count == 3:
            return(O)


    # These are the coordinates of the diagonal cells for left-right diagonal
    lr_diagonal = [[0,0],[1,1],[2,2]]
    # For right-left diagonal
    rl_diagonal = [[0,2],[1,1],[2,0]]
    mocklr = []
    mockrl = []

    # Append the elements in the lr diagonal to an empty list
    for i in lr_diagonal:
        mocklr.append(board[i[0]][i[1]])
    # Append the elements in the rl diagonal to an empty list
    for i in rl_diagonal:
        mockrl.append(board[i[0]][i[1]])

    # Check if there is a three in a row in these diagonals
    x_countlr = mocklr.count(X)
    o_countlr = mocklr.count(O)
    if x_countlr == 3:
        return (X)
    if o_countlr == 3:
        return(O)

    x_countrl = mockrl.count(X)
    o_countrl = mockrl.count(O)
    if x_countrl == 3:
        return (X)
    if o_countrl == 3:
        return(O)

    # If all if statements are not met then there is no winner
    return(None)

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) is not None:
        # if there is one game is over
        return True

    counter = 0

    # Check if all cells have been played
    for i in board:
        if EMPTY in i:
            counter += 1
    # No more empty cells are available in the board
    if counter == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check for winners
    if winner(board) == X:
        return (1)
    if winner(board) == O:
        return(-1)
    if winner(board) is None:
        return(0)

def max_value(board):
    # Check if its a terminal board then return the utility value
    if terminal(board):
        return(utility(board))
    # Set a mock value for v
    v = -math.inf
    # Calculate the max value of v for all possible actins
    for action in actions(board):
        v = max(v,min_value(result(board,action)))
    return v

def min_value(board):
    # Check if its a terminal board then return the utility value
    if terminal(board):
        return(utility(board))
    # Set a mock value for v
    v = math.inf
    # Calculate the min value of v for all possible actins
    for action in actions(board):
        v = min(v,max_value(result(board,action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    move = None

    if player(board) == X:
        best_val = -math.inf
        for action in actions(board):
            temp = min_value(result(board,action))
            if temp > best_val:
                best_val = temp
                move = action

    if player(board) == O:
        best_val = math.inf
        for action in actions(board):
            temp = max_value(result(board,action))
            if temp < best_val:
                best_val = temp
                move = action
    return (move)
