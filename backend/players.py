import random
import os
import pickle

# Define constants to use throughout the game
BLANK = ' '
AI_PLAYER = 'X'
HUMAN_PLAYER = 'O'

# Base class for both human and AI players
class Player:

    def show_board(self, board, message=''):
        # Clear the terminal for a clean display
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n= Tic Tac Toe =\n")
        for i in range(0, 9, 3):
            # Print 3 cells per row
            print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
            if i < 6:
                print("---|---|---")
        if message:
            print(f"[ {message} ]\n")

# Human player doesn't need learning or feedback
class HumanPlayer(Player):
    def reward(self, value, board):
        pass

# AI player that learns over time
class AIPlayer(Player):
    def __init__(self, epsilon=0.9, alpha=0.5, gamma=0.5, default_q=1):
        # Learning parameters
        self.EPSILON = epsilon  # Exploration: how often to try random moves
        self.ALPHA = alpha      # Learning rate: how fast to learn from results
        self.GAMMA = gamma      # Discount factor: how much future matters
        self.DEFAULT_Q = default_q  # Default Q-value if not learned yet

        # Memory and state
        self.q = {}             # Q-table: maps (state, action) → value
        self.move = None        # Last move made
        self.board = (' ',) * 9 # Last board state
        self.games_played = 0   # How many full games this AI has seen

        self.adjust_difficulty()  # Adjust difficulty at start

    def adjust_difficulty(self):
        # Change learning settings based on experience level
        if self.games_played < 2:
            self.EPSILON = 0.9   # Easy: mostly random
            self.ALPHA = 0.5
            self.GAMMA = 0.5
        elif self.games_played < 4:
            self.EPSILON = 0.4   # Medium: mixes strategy and exploration
            self.ALPHA = 0.3
            self.GAMMA = 0.9
        else:
            self.EPSILON = 0.05  # Hard: mostly strategic and stable
            self.ALPHA = 0.1
            self.GAMMA = 0.95

    def available_moves(self, board):
        # Return all indexes where the board is still blank
        return [i for i in range(9) if board[i] == BLANK]

    def get_q(self, state, action):
        # Look up the Q-value for (state, action); if not there, return default
        if (state, action) not in self.q:
            self.q[(state, action)] = self.DEFAULT_Q
        return self.q[(state, action)]

    def make_move(self, board):
        # Save the board state as a tuple so it's hashable in the Q-table
        self.board = tuple(board)
        actions = self.available_moves(board)

        # Choose between exploration (random) or exploitation (best Q)
        if random.random() < self.EPSILON:
            self.move = random.choice(actions)  # Try something new
        else:
            q_values = [self.get_q(self.board, a) for a in actions]
            max_q = max(q_values)
            best = [a for a, q in zip(actions, q_values) if q == max_q]
            self.move = random.choice(best)     # Choose the best known move

        return self.move

    def reward(self, reward, board):
        # Apply learning only if a move was made
        if self.move is not None:
            prev_q = self.get_q(self.board, self.move)

            # Estimate the best possible future reward from the new board
            max_q = max(
                [self.get_q(tuple(board), a) for a in self.available_moves(board)],
                default=0
            )

            # Update Q-value using the Q-learning formula
            self.q[(self.board, self.move)] = prev_q + self.ALPHA * (reward + self.GAMMA * max_q - prev_q)

            # Update experience count
            self.games_played += 1

            # Adjust learning strategy as experience grows
            self.adjust_difficulty()

            # Save updated Q-table to disk
            self.save_q_table()

    def save_q_table(self, filename="q_table.pkl"):
        # Save Q-table and games played to a file so AI remembers its training
        with open(filename, "wb") as f:
            pickle.dump({
                "q": self.q,
                "games_played": self.games_played
            }, f)

    def load_q_table(self, filename="q_table.pkl"):
        # Load existing Q-table and experience if available
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                try:
                    data = pickle.load(f)
                    self.q = data.get("q", {})
                    self.games_played = data.get("games_played", 0)
                    self.adjust_difficulty()  # Match settings to experience
                except EOFError:
                    self.q = {}
                    self.games_played = 0
        else:
            self.q = {}
            self.games_played = 0
