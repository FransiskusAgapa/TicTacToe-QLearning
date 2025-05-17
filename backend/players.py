import random
import os
import pickle

BLANK = ' '
AI_PLAYER = 'X'
HUMAN_PLAYER = 'O'

class Player:

    def show_board(self, board, message=''):
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n= Tic Tac Toe =\n")
        for i in range(0, 9, 3):
            print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
            if i < 6:
                print("---|---|---")
        if message:
            print(f"[ {message} ]\n")

class HumanPlayer(Player):
    def reward(self, value, board):
        pass

class AIPlayer(Player):
    def __init__(self, epsilon=0.4, alpha=0.3, gamma=0.9, default_q=1):
        self.EPSILON = epsilon
        self.ALPHA = alpha
        self.GAMMA = gamma
        self.DEFAULT_Q = default_q
        self.q = {}
        self.move = None
        self.board = (' ',) * 9

    def available_moves(self, board):
        return [i for i in range(9) if board[i] == ' ']

    def get_q(self, state, action):
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = self.DEFAULT_Q
        return self.q[(state, action)]

    def make_move(self, board):
        self.board = tuple(board)
        actions = self.available_moves(board)
        if random.random() < self.EPSILON:
            self.move = random.choice(actions)
        else:
            q_values = [self.get_q(self.board, a) for a in actions]
            max_q = max(q_values)
            best = [a for a, q in zip(actions, q_values) if q == max_q]
            self.move = random.choice(best)
        return self.move

    def reward(self, reward, board):
        if self.move is not None:
            prev_q = self.get_q(self.board, self.move)
            max_q = max(
                    [
                        self.get_q(tuple(board), a) 
                        for a in self.available_moves(board)
                    ], 
                    default=0
                )
            self.q[(self.board, self.move)] = prev_q + self.ALPHA * (reward + self.GAMMA * max_q - prev_q)

    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q, f)

    def load_q_table(self, filename="q_table.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                try:
                    self.q = pickle.load(f)
                except EOFError:
                    self.q = {}
        else:
            self.q = {}