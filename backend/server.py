# server.py

from flask import Flask, request, jsonify
from players import AIPlayer, AI_PLAYER, HUMAN_PLAYER
from engine import TicTacToe

app = Flask(__name__)
game = TicTacToe()
ai = AIPlayer()
ai.load_q_table()

REWARD_WIN = 10
REWARD_LOSE = -10
REWARD_TIE = -3

@app.route("/api/new", methods=["GET"])
def new_game():
    global game
    game = TicTacToe()
    return jsonify({
            "board": game.board, 
            "current_turn": game.current_turn
        })

@app.route("/api/move", methods=["POST"])
def move():
    data = request.json
    user_move = data.get("move")

    # Human plays
    if not game.apply_move(user_move, HUMAN_PLAYER):
        return jsonify({
            "error": "Invalid move"
            }), 400

    winner = game.get_winner()
    if winner:
        if winner == HUMAN_PLAYER:
            ai.reward(REWARD_LOSE, game.board)
        elif winner == AI_PLAYER:
            ai.reward(REWARD_WIN, game.board)
        elif winner == "Tie":
            ai.reward(REWARD_TIE, game.board)
        return jsonify({
            "board": game.board, 
            "winner": winner
            })

    # AI plays
    ai_move = ai.make_move(game.board)
    game.apply_move(ai_move, AI_PLAYER)

    winner = game.get_winner()
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
        "winner": winner
    })

@app.route("/api/reset", methods=["GET"])
def reset_game():
    global game
    game = TicTacToe()
    return jsonify({
            "board": game.board, 
            "current_turn": game.current_turn
        })

if __name__ == "__main__":
    app.run(debug=True)

