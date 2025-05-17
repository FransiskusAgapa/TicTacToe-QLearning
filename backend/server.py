# Import tools to build the web server and handle requests/responses
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import the AI logic and game engine
from players import AIPlayer, AI_PLAYER, HUMAN_PLAYER
from engine import TicTacToe

# Create the Flask app — like opening a window to let others talk to the game
app = Flask(__name__)

# Allow the frontend (browser) to send and receive data from this backend
CORS(app)

# Set up the main game instance and AI player — just one shared game per session
game = TicTacToe()
ai = AIPlayer()
ai.load_q_table()  # Load previous training data (Q-values) if available

# Define rewards that guide the AI’s learning behavior
REWARD_WIN = 10        # Reward the AI if it wins
REWARD_LOSE = -10      # Punish the AI if it loses
REWARD_TIE = -3        # Slight penalty for drawing — to encourage better strategy

# Endpoint to start a fresh new game (used when app loads or user clicks "Play Again")
@app.route("/api/new", methods=["GET"])
def new_game():
    global game
    game = TicTacToe()  # Start from a blank board
    print("⚠️ /api/new called")
    return jsonify({
        "board": game.board,
        "current_turn": game.current_turn
    })

# Endpoint to handle a move made by the human player and then by the AI
@app.route("/api/move", methods=["POST"])
def move():
    data = request.json
    user_move = data.get("move")
    ai_move = None 

    # Human makes a move
    if not game.apply_move(user_move, HUMAN_PLAYER):
        return jsonify({ "error": "Invalid move" }), 400

    # Check if the human won
    winner, combo = game.get_winner()
    if winner:
        if winner == HUMAN_PLAYER:
            ai.reward(REWARD_LOSE, game.board)
        elif winner == AI_PLAYER:
            ai.reward(REWARD_WIN, game.board)
        elif winner == "Tie":
            ai.reward(REWARD_TIE, game.board)

        return jsonify({
            "board": game.board,
            "ai_move": ai_move, 
            "winner": winner,
            "winning_combo": combo
        })

    # Let AI play if human didn't win
    ai_move = ai.make_move(game.board)
    game.apply_move(ai_move, AI_PLAYER)

    winner, combo = game.get_winner()
    if winner:
        if winner == HUMAN_PLAYER:
            ai.reward(REWARD_LOSE, game.board)
        elif winner == AI_PLAYER:
            ai.reward(REWARD_WIN, game.board)
        elif winner == "Tie":
            ai.reward(REWARD_TIE, game.board)

    return jsonify({
        "board": game.board,
        "ai_move": ai_move,     # now guaranteed to exist
        "winner": winner,
        "winning_combo": combo
    })

# Endpoint to reset the board manually without refreshing the browser
@app.route("/api/reset", methods=["GET"])
def reset_game():
    global game
    game = TicTacToe()  # Reinitialize the board
    return jsonify({
        "board": game.board,
        "current_turn": game.current_turn
    })

# Start the backend server so it can receive requests
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode prints helpful info in the terminal