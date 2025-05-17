# Import player symbols so we can reference 'X' and 'O'
from players import AI_PLAYER, HUMAN_PLAYER

# This class handles everything related to the game board and rules
class TicTacToe:
    def __init__(self):
        # Create a blank 3x3 board using a list of 9 spaces
        self.board = [' '] * 9

        # The human always starts first by default
        self.current_turn = HUMAN_PLAYER

    # Apply a player's move to the board
    def apply_move(self, move, player):
        # If the cell is empty, we allow the move
        if self.board[move] == ' ':
            self.board[move] = player  # Mark the board with the player's symbol
            # Switch turns: if human moved, AI goes next — and vice versa
            self.current_turn = AI_PLAYER if player == HUMAN_PLAYER else HUMAN_PLAYER
            return True  # Move was accepted
        return False  # Move was invalid (cell already taken)

    # Determine if there's a winner or a tie
    def get_winner(self):
        b = self.board  # Shortcut for easier reading

        # These are the 8 possible winning combinations (rows, cols, diagonals)
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # horizontal rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # vertical columns
            [0, 4, 8], [2, 4, 6]              # diagonal lines
        ]

        # Loop through each possible win combination
        for combo in combos:
            # Check if the 3 positions in this combo all have the same symbol
            if b[combo[0]] == b[combo[1]] == b[combo[2]] != ' ':
                # If so, return the winner symbol and the winning positions
                return b[combo[0]], combo

        # If no winner and no empty spots, it's a tie
        if ' ' not in b:
            return 'Tie', []

        # Otherwise, the game is still ongoing
        return None, []

    # Return a list of indexes for empty cells (valid move options)
    def available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']