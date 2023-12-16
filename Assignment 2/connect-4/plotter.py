import time
import numpy as np
import random
import math
from agent import Agent
import copy
import json
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, check_piece):
    # Check horizontal locations for win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == check_piece and board[row][col+1] == check_piece and board[row][col+2] == check_piece and board[row][col+3] == check_piece:
                return True

    # Check vertical locations for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col] == check_piece and board[row+1][col] == check_piece and board[row+2][col] == check_piece and board[row+3][col] == check_piece:
                return True

    # Check positively sloped diaganols
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == check_piece and board[row+1][col+1] == check_piece and board[row+2][col+2] == check_piece and board[row+3][col+3] == check_piece:
                return True

    # Check negatively sloped diaganols
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == check_piece and board[row-1][col+1] == check_piece and board[row-2][col+2] == check_piece and board[row-3][col+3] == check_piece:
                return True

def evaluate_window(window, turn_piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if turn_piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(turn_piece) == 4:
        score += 100
    elif window.count(turn_piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(turn_piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position(board, check_piece):
    score = 0
    # Score center column
    center_arr = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_arr.count(check_piece)
    score += center_count * 3
    # Score Horizontal
    for row in range(ROW_COUNT):
        row_arr = [int(i) for i in list(board[row, :])]
        for col in range(COLUMN_COUNT-3):
            window = row_arr[col:col+WINDOW_LENGTH]
            score += evaluate_window(window, check_piece)
    # Score Vertical
    for col in range(COLUMN_COUNT):
        col_arr = [int(i) for i in list(board[:, col])]
        for row in range(ROW_COUNT-3):
            window = col_arr[row:row+WINDOW_LENGTH]
            score += evaluate_window(window, check_piece)
    # Score posiive sloped diagonal
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3):
            window = [board[row+i][col+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, check_piece)
    # Score negative sloped diagonal
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3):
            window = [board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, check_piece)
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def bot_player(board, piece, opp_piece):
    bot = piece
    opponent = opp_piece
    valid_cols = get_valid_locations(board)
    col_move = random.choice(valid_cols)
    # block horizontal
    for row in range(0, ROW_COUNT):
        row = []
        for col in range(0, COLUMN_COUNT-4):
            row = [board[row][col], board[row][col+1], board[row][col+2], board[row][col+3]]
            if row.count(opponent) == 3 and row.count(0) == 1:
                if row == 0:
                    col_move = col + row.index(0)
                elif board[row-1][col + row.index(0)] != 0:
                    col_move = col + row.index(0)

    # block vertical
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT):
            if board[row][col] == opponent and board[row+1][col] == opponent and board[row+2][col] == opponent:
                if row+3 < ROW_COUNT:
                    if board[row+3][col] == 0:
                        col_move = col

    # block diagonal
    for row in range(ROW_COUNT-3):
        diag = []
        for col in range(COLUMN_COUNT-3):
            diag = [board[row][col], board[row+1][col+1],
                    board[row+2][col+2], board[row+3][col+3]]
            if diag.count(opponent) == 3 and diag.count(0) == 1:
                temp = col + diag.index(0)
                if diag.index(0) == 0 and row == 0:
                    col_move = temp
                elif board[row+diag.index(0)-1][temp] != 0:
                    col_move = temp

    # block anti-diagonal
    for row in range(3, ROW_COUNT):
        diag = []
        for col in range(0, COLUMN_COUNT-3):
            diag = [board[row][col], board[row-1][col+1],
                    board[row-2][col+2], board[row-3][col+3]]
            if diag.count(opponent) == 3 and diag.count(0) == 1:
                temp = col + diag.index(0)
                if diag.index(0) == 3 and row == 0:
                    col_move = temp
                elif board[row-diag.index(0)-1][temp] != 0:
                    col_move = temp

    # fill horizontal
    for row in range(0, ROW_COUNT):
        row = []
        for col in range(0, COLUMN_COUNT-4):
            row = [board[row][col], board[row][col+1], board[row][col+2], board[row][col+3]]
            if row.count(bot) == 3 and row.count(0) == 1:
                if row == 0:
                    col_move = col + row.index(0)
                elif board[row-1][col + row.index(0)] != 0:
                    col_move = col + row.index(0)

    # fill vertical
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT):
            if board[row][col] == bot and board[row+1][col] == bot and board[row+2][col] == bot:
                if row+3 < ROW_COUNT:
                    if board[row+3][col] == 0:
                        col_move = col

    # fill diagonal
    for row in range(ROW_COUNT-3):
        diag = []
        for col in range(COLUMN_COUNT-3):
            diag = [board[row][col], board[row+1][col+1],
                    board[row+2][col+2], board[row+3][col+3]]
            if diag.count(bot) == 3 and diag.count(0) == 1:
                temp = col + diag.index(0)
                if diag.index(0) == 0 and row == 0:
                    col_move = temp
                elif board[row+diag.index(0)-1][temp] != 0:
                    col_move = temp

    # fill anti-diagonal
    for row in range(3, ROW_COUNT):
        diag = []
        for col in range(0, COLUMN_COUNT-3):
            diag = [board[row][col], board[row-1][col+1],
                    board[row-2][col+2], board[row-3][col+3]]
            if diag.count(bot) == 3 and diag.count(0) == 1:
                temp = col + diag.index(0)
                if diag.index(0) == 3 and row == 0:
                    col_move = temp
                elif board[row-diag.index(0)-1][temp] != 0:
                    col_move = temp
    return col_move

def minimax(b, d, a, beta, mP):
    valid_locations = get_valid_locations(b)
    is_terminal = is_terminal_node(b)
    if d == 0 or is_terminal:
        if is_terminal:
            if winning_move(b, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(b, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(b, AI_PIECE))
    if mP:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(b, col)
            b_copy = b.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, d-1, a, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            a = max(a, value)
            if a >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(b, col)
            b_copy = b.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, d-1, a, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if a >= beta:
                break
        return column, value


var = 0
arr = []
for i in tqdm(range(1000)):
    # CONSTANTS
    ROW_COUNT = 5
    COLUMN_COUNT = 5
    EMPTY = 0
    PLAYER_PIECE = -1
    AI_PIECE = 1
    WINDOW_LENGTH = 4
    moves = 0
    board = create_board()
    game_over = False
    q_agent = Agent()
    AI = 1
    PLAYER = 0
    q_values_file_f = "q_values_f.pkl"  # playing first
    q_values_file_s = "q_values_s.pkl"  # playing second

    if not os.path.exists(q_values_file_f):
        q_agent.learn(AI, 100000)
        q_agent.q_learner.save_values(q_values_file_f)
        q_agent.learn(PLAYER, 100000)
        q_agent.q_learner.save_values(q_values_file_s)
    else:
        q_agent.q_learner.load_values(q_values_file_f)

    turn = 1

    while not game_over:
        if turn == AI and not game_over:
            moves += 1
            # Q LEARNING
            c_board = copy.copy(board)
            c_board = c_board.tolist()
            int_list = [[int(x) for x in sublist] for sublist in c_board]
            board_str = json.dumps(int_list)
            col = q_agent.q_learner.get_best_action(board_str)
            if col == None:
                col = random.choice(get_valid_locations(board))

            # MINIMAX PLAYER
            # col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    arr.append(1)
                    game_over = True
                turn = PLAYER

        elif turn == PLAYER and not game_over:
            moves += 1
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    arr.append(-1)
                    game_over = True
                turn = AI

        if moves == ROW_COUNT * COLUMN_COUNT:
            arr.append(0)
            game_over = True

x_win, y_win = [], []
x_tie, y_tie = [], []
x_loss, y_loss = [], []

# Loop through the results and append the x and y values to the appropriate list
for i, result in enumerate(arr):
    if result == 1:
        x_win.append(i)
        y_win.append(result)
    elif result == 0:
        x_tie.append(i)
        y_tie.append(result)
    else:
        x_loss.append(i)
        y_loss.append(result)

# Plot each outcome separately with a different color and marker
plt.scatter(x_win, y_win, c='blue', marker='o', label='Player wins')
plt.scatter(x_tie, y_tie, c='red', marker='s', label='Tie')
plt.scatter(x_loss, y_loss, c='black', marker='x', label='Player loses')
plt.ylabel("Outcomes")
plt.xlabel("Iterations")
# Add a legend with the three labels
plt.legend()

# Show the plot
plt.show()

unique, counts = np.unique(arr, return_counts=True)
percentages = counts / len(arr)
print(percentages)
plt.hist(arr, bins=[-1, 0, 1, 2], align='left',
         weights=np.zeros_like(arr) + 1. / len(arr))
plt.ylabel('Percentage')
plt.xticks([-1, 0, 1], ['-1 (Player 1 loses)', '0 (Tie)', '1 (Player 1 wins)'])
plt.xlabel('Outcome')
plt.title('Results of 1000 Connect 4 Games')
plt.show()

unique, counts = np.unique(arr, return_counts=True)
percentages = counts / len(arr) * 100
plt.pie(counts, labels=unique, autopct='%1.1f%%')
plt.title('Results of 1000 Connect 4 Games')
plt.show()
