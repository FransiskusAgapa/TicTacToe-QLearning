# engine.py

from players import AI_PLAYER, HUMAN_PLAYER

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_turn = HUMAN_PLAYER

    def apply_move(self, move, player):
        if self.board[move] == ' ':
            self.board[move] = player
            self.current_turn = AI_PLAYER if player == HUMAN_PLAYER else HUMAN_PLAYER
            return True
        return False

    def get_winner(self):
        b = self.board
        for i in range(3):

            # Horizontal checker
            if b[3*i] == b[3*i+1] == b[3*i+2] != ' ':
                return b[3*i]
            
            # Vertical checker 
            if b[i] == b[i+3] == b[i+6] != ' ':
                return b[i]
        
        # Diagonal checker
        if b[0] == b[4] == b[8] != ' ' or b[2] == b[4] == b[6] != ' ':
            return b[4]
        
        # all spots taken
        if ' ' not in b:
            return 'Tie'
        
        return None

    # Check empty spots
    def available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']
