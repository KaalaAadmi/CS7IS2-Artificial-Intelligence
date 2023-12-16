ROW_COUNT = 5
COLUMN_COUNT = 5

class Connect4:
    def __init__(self):
        self.board = [[0 for _ in range(ROW_COUNT)] for _ in range(COLUMN_COUNT)]
        self.player = -1

    # Get the winner of the game
    def _get_winner(self):
        # Check horizontal
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT-3):
                if abs(sum(self.board[r][c:c+4])) == 4:
                    return self.board[r][c]
        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if abs(sum(self.board[r+i][c] for i in range(4))) == 4:
                    return self.board[r][c]
        # Check diagonal (positive slope)
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                if abs(sum(self.board[r+i][c+i] for i in range(4))) == 4:
                    return self.board[r][c]
        # Check diagonal (negative slope)
        for r in range(ROW_COUNT-3):
            for c in range(3, COLUMN_COUNT):
                if abs(sum(self.board[r+i][c-i] for i in range(4))) == 4:
                    return self.board[r][c]

        return None

    # Get the current state of the game
    def get_state(self):
        return str(self.board)

    # Get valid actions (open columns) for the current game state
    def get_valid_actions(self):
        act = []
        for c in range(COLUMN_COUNT):
            if self.board[ROW_COUNT-1][c] == 0:
                act.append(c)
        return act

    # Check if the game has ended
    def is_ended(self):
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if self.board[r][c] == 0:
                    return False
        return True

    # Play a move in the specified column
    def play(self, c):
        if self.board[ROW_COUNT-1][c] != 0:
            return None

        for r in range(ROW_COUNT):
            if self.board[r][c] == 0:
                self.board[r][c] = self.player
                break

        winner = self._get_winner()
        if winner:
            return winner
        self.player *= -1
        return None
