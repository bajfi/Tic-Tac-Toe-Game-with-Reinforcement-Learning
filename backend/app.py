import os

import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from model import Player, State

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

# Configure static file serving
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Initialize the AI player
ai_player = Player(epsilon=0)  # No exploration during gameplay
ai_player.set_symbol(-1)  # AI plays as O (-1)
ai_player.load_policy()


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


@app.route("/api/move", methods=["POST"])
def get_ai_move():
    try:
        board = request.json.get("board")
        # Convert board to numpy array
        board_state = np.zeros((3, 3), dtype=np.int32)
        for i, mark in enumerate(board):
            if mark == "X":
                board_state[i // 3, i % 3] = 1
            elif mark == "O":
                board_state[i // 3, i % 3] = -1

        # Create state to check if game is over
        state = State()
        state.data = board_state
        if state.is_end():
            return jsonify({"error": "Game is already over"}), 400

        # Set state and get AI move
        ai_player.set_state(state)
        move = ai_player.act()
        if move is None:
            return jsonify({"error": "No valid moves"}), 400

        # Convert 2D position to 1D index
        move_idx = move[0] * 3 + move[1]
        return jsonify({"move": move_idx})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset_game():
    ai_player.reset()
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)
