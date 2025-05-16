"""
“Hey, I’m going to flip coins and roll dice sometimes, 
so I need randomness!”
"""
import random 

import os 

"""
“Okay, I’ll use 
'X' to mark the AI, 
'O' for humans, 
' ' (a space) for empty tiles.”
"""
BLANK = ' '
AI_PLAYER = 'X'
HUMAN_PLAYER = 'O'


"""
“I’m going to train the AI by letting it play 40,000 games.
And in each game, I’ll give it a 40% chance 
to just try something new, even if it doesn't seem smart. 
Why? Because that's how we discover new tricks — exploration!”
"""
TRAINING_EPOCHS = 10
TRAINING_EPSILON = 0.4 # try % of new move 


"""
“Let’s set the prize money:
Win = 10 points,
Lose =  lose 10 points,
Tie = lose a few points (no one likes ties here).”
"""
REWARD_WIN = 10 
REWARD_LOSE = -10
REWARD_TIE = -3

"""
“This is the parent template for 
both human and AI players.”
"""
class Player: 

    """
    “Hey, here’s how we’ll print the game board 
    like a 3x3 grid.”
    @staticmethod : a regular function but is placed 
                inside a class for organizational purposes.
    """
    @staticmethod
    def show_board(board):

        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Show board with reference numbers for empty spots
        def format_cell(i):
            return board[i] if board[i] != ' ' else str(i + 1)

        print("\n")
        print(f" {format_cell(0)} | {format_cell(1)} | {format_cell(2)} ")
        print("---|---|---")
        print(f" {format_cell(3)} | {format_cell(4)} | {format_cell(5)} ")
        print("---|---|---")
        print(f" {format_cell(6)} | {format_cell(7)} | {format_cell(8)} ")
        print("\n")

    


class HumanPlayer(Player):

    def reward(self, value,board):
        pass 

    """
    “Ask the human, ‘Hey, where do you want to play (1–9)?’
    Keep asking if they say something silly
    """
    def make_move(self,board):

        while True: 
            try: 
                self.show_board(board)
                move = input("Your next move (cell index 1 - 9): ")
                move = int(move)

                if not (move - 1 in range(9)):
                    raise ValueError 
            except ValueError:
                print("\n! Invalid move, try again")
            else:
                return move-1 # cause computer counts from 0, but you count from 1.”


"""
“Meet the AI! This one doesn’t guess,
where it learns by trial and error.”
"""
class AIPlayer(Player):

    """
    'epsilon'  : probability of exploration | 'How curious is it?'
    'alpha'    : learning rate | 'How quickly does it learn from mistakes?'
    'gamma'    : reward in the future | 'How much is cares about future rewards?'
    'default_q : given move at a given state | Its memory of moves it tried and how well they worked.”
    """
    def __init__(self,epsilon=0.4, alpha=0.3,gamma=0.9,default_q=1):
        self.EPSILON = epsilon
        self.ALPHA = alpha 
        self.GAMMA = gamma
        self.DEFAULT_Q = default_q 

        """
        Q(s,a) = Q(state, action) a pair
        “Every time I play, I take a photo of the board 
        (state), and write in my diary:
        ‘If I play here (action), 
        how did it go?’ That’s Q(state, action).”
        """
        self.q = {}

        # previous move during the game
        self.move = None

        # store actual board in previous iteration 
        self.board = (' ',) * 9

    """
    “Let’s make a to-do list of all empty spots 
    where I can move.”
    """
    # Available / empty cell
    def available_moves(self,board):
        return [i for i in range(9) if board[i] == ' ']
    
    """
    “If I’ve never seen this situation before, 
    I assume it’s worth 1 point.
    Later, I’ll update this if it’s actually a smart 
    or dumb move.”
    """
    # Q(s,a) -> Q value for (s,a) pair. create new pair if no pair exist
    # default value (=1) otherwise the pair
    def get_q(self,state,action):
        if self.q.get((state,action)) is None:
            self.q[(state,action)] = self.DEFAULT_Q 
        return self.q[(state,action)]


    """
    make a random move with epsilon probability (exploration) or
    pick action with the highest Q value (exploitation)
    -
    40% of the time, I’ll just try something random (explore).
    60% of the time, I’ll look at my diary (Q-table) and pick the best move I know.”
    """
    def make_move(self,board):
        
        self.board = tuple(board) # immutable
        actions = self.available_moves(board) # 1d array

        # action with epsilon probability (exploration)
        if random.random() < self.EPSILON:
            # this is 0-8 index
            self.move = random.choice(actions)
            return self.move 
        
        # take actions with highest Q value (exploitation)
        q_values = [self.get_q(self.board, a) for a in actions]
        max_q_values = max(q_values)

        # if multiple best actions, choose one at random 
        if q_values.count(max_q_values) > 1: 
            best_actions = [i for i in range(len(actions)) if q_values[i] == max_q_values]
            best_move = actions[random.choice(best_actions)] # pick one at random 
        else:
            best_move = actions[q_values.index(max_q_values)]

        self.move = best_move 
        return self.move


    """
    “Okay, game’s over. Let’s learn from what just happened.
    I look back at my last move (the one I just made),
    See how good the outcome was,
    Then update my memory: ‘If I see this board again, 
    should I do that move again?’”
    -
    It's doing (how it slowly improves):
    Old Value ← Old + Learning Rate × (Reward + Future Potential − Old)
    """
    def reward(self,reward, board):
        if self.move:
            prev_q = self.get_q(self.board,self.move)
            max_q_new = max([self.get_q(tuple(board),a) for a in self.available_moves(self.board)])
            self.q[(self.board,self.move)] = prev_q + self.ALPHA * (reward + self.GAMMA * max_q_new- prev_q)


"""
“This is the game master. It manages players, 
turns, wins, losses, and draws.”
"""
# Game Logic
class TicTacToe:
    
    def __init__(self, player1,player2):
        self.player1 = player1 
        self.player2 = player2 
        self.first_player_turn = random.choice([True,False]) # randomly generated
        self.board = [' '] * 9 # empty board at the start (1D)

    """
    “Let’s run the whole game like a 
    loop until someone wins or we tie.”
    """
    def play(self):

        # game loop 
        while True: 
            if self.first_player_turn:
                player = self.player1 
                other_player = self.player2
                # During training purpose consider both players are AI
                player_tickers = (AI_PLAYER, HumanPlayer)
            else: 
                player = self.player2 
                other_player = self.player1
                player_tickers = (HUMAN_PLAYER, AI_PLAYER)

            # check the game state (win , lose, draw)
            game_over , winner = self.is_game_over(player_tickers)

            # handle rewards when game over
            if game_over:
                if winner == player_tickers[0]:
                    player.show_board(self.board[:])

                    print(f"\nWinner: {player.__class__.__name__}")
                    player.reward(REWARD_WIN, self.board[:]) # reward for algorithm learning,
                    other_player.reward(REWARD_LOSE, self.board[:])
                elif winner == player_tickers[1]:
                    player.show_board(self.board[:])
                    print(f"\nWinner: {other_player.__class__.__name__}")
                    other_player.reward(REWARD_WIN, self.board[:])
                    player.reward(REWARD_LOSE, self.board[:])
                else: 
                    player.show_board(self.board[:])
                    print("\nTie")
                    player.reward(REWARD_TIE,self.board[:])
                break
            
            # next player's turn in the next iteration 
            self.first_player_turn = not self.first_player_turn # let other player to start first  in next game

            # actual player'  best move best on Q(s,a)
            move = player.make_move(self.board)
            self.board[move] = player_tickers[0]


    """
    “Let’s check if anyone has won:
    """
    def is_game_over(self,player_tickers):

        # consider both players ('X' and 'O' players)
        for player_ticker in player_tickers:
            
            # Horizontal check
            for i in range(3):
                if self.board[3 * i + 0] == player_ticker and self.board[3 * i + 1] == player_ticker and self.board[3 * i + 2] == player_ticker:
                    return True, player_ticker

            # Vertical check 
            for j in range(3):
                if self.board[j + 0] == player_ticker and self.board[j + 3] == player_ticker and self.board[j + 6] == player_ticker:
                    return True, player_ticker
            
            # Diagonal check (top left to bottom right + top right to bottom left)
            if self.board[0] == player_ticker and self.board[4] == player_ticker and self.board[8] == player_ticker:
                return True, player_ticker
            
            # 
            if self.board[2] == player_ticker and self.board[4] == player_ticker and self.board[6] == player_ticker:
                return True, player_ticker 

        # Draw
        if self.board.count(' ') == 0:
                return True, None 
        else: 
                return False, None # not the end of the game 


"""
“This is the starting line.”
"""
if __name__ == "__main__":

    """
    It sets up two AI players 
    and lets them train by playing 
    thousands of games.
    """
    ai_player_1 = AIPlayer()
    ai_player_2 = AIPlayer()

    print("\n> AI Training has started")

    ai_player_1.EPSILON = TRAINING_EPSILON
    ai_player_2.EPSILON = TRAINING_EPSILON

    for _ in range(TRAINING_EPOCHS):
        game = TicTacToe(ai_player_1, ai_player_2)
        game.play()

    print("\n> AI Training has ended.")

    ai_player_1.EPSILON = 0 
    human_player = HumanPlayer() 
    game = TicTacToe(ai_player_1, human_player)
    game.play()