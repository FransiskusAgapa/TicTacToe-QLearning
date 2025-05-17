#  Tic Tac Toe vs AI — Web App 
## (language was written by ChatGPT)

Play classic Tic Tac Toe against an AI that learns over time!
This app runs in your browser and talks to a Python backend that uses **Q-Learning** to get smarter the more you play.

---

##  How It Works

* The frontend is built with **HTML/CSS/JavaScript**
* The backend is a simple **Flask API**
* The AI uses **Q-Learning** to make better moves as it trains
* The board will **freeze** after a win or tie so you can see the result
* You can click **“Play Again”** to start a new game

---

##  Getting Started

### 1. Clone or Download

```bash
git clone https://github.com/your-repo/tictactoe-ai.git
cd tictactoe-ai
```

### 2. Set up the backend

Install Python dependencies:

```bash
pip install flask flask-cors
```

Then run the Flask server:

```bash
python server.py
```

### 3. Open the game

Simply open `index.html` in your browser.

If you prefer running a local server:

```bash
python -m http.server 5500
```

Then visit:
`http://127.0.0.1:5500/index.html`

---

## How to Play

1. Click “Start Play” to begin.
2. You (O) go first. Click an empty square.
3. The AI (X) will respond with its move.
4. The game will freeze when someone wins or it's a tie.
5. Click **“Play Again”** to reset and play again.

---

## Tech Used

*  Q-Learning algorithm
*  Flask (Python backend)
*  HTML/CSS/JavaScript frontend
*  Real-time communication via REST API

---

##  Bonus Challenge — Can You Solve the Restart Bug?

>  Sometimes, the game **restarts by itself** after a win — without you pressing the button.

Even ChatGPT had trouble tracking this down at first.

### Your Challenge:

Find out what part of the code (JS or server) **triggers the restart** after a game ends — even though:

* The backend does NOT reset itself
* The frontend says `startNewGame()` is never called

Use `console.trace()`, browser DevTools, and debugging skills to **find the secret restart trigger**.

Post your answer as a GitHub Issue or share it with your team.
(And no, it’s not in `server.py` )
---