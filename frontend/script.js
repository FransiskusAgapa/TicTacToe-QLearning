// ======================
// === GLOBAL STATES ===
// ======================

// This holds the current game board (9 spots, empty at first)
let board = Array(9).fill(" ");

// Tracks whose turn it is (human goes first)
let isHumanTurn = true;

// Whether the game is over (win or draw freezes it)
let gameOver = false;

// Reference to the HTML board, message display, and button
const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const resetBtn = document.getElementById("resetBtn");

// ===========================
// === RESET ONLY WHEN TOLD ===
// ===========================

resetBtn.addEventListener("click", () => {
    fetch("http://127.0.0.1:5000/api/new")
        .then(res => res.json())
        .then(data => {
            board = data.board;            // New empty board from backend
            isHumanTurn = true;            // Human goes first again
            gameOver = false;              // Game is active again
            statusEl.textContent = "Your Turn!";
            renderBoard();                 // Draw it!
        });
});

// ========================
// === RENDER THE BOARD ===
// ========================

function renderBoard(winningCombo = []) {
    boardEl.innerHTML = ""; // clear all grid

    board.forEach((cell, index) => {
        const cellEl = document.createElement("div");
        cellEl.classList.add("cell");
        cellEl.textContent = cell;

        // Highlight win combo if game ended
        if (winningCombo.includes(index)) {
            cellEl.classList.add("winner");
        }

        // Only allow click if it's not over, it's human's turn, and the cell is blank
        if (cell === " " && isHumanTurn && !gameOver) {
            cellEl.addEventListener("click", () => makeMove(index));
        } else {
            cellEl.classList.add("disabled"); // Can't touch this
        }

        boardEl.appendChild(cellEl);
    });
}

// ===========================
// === MAKE HUMAN MOVE ===
// ===========================

function makeMove(index) {
    if (gameOver) return; // If game is frozen, do nothing

    fetch("http://127.0.0.1:5000/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ move: index })
    })
    .then(res => res.json())
    .then(data => {
        board = data.board; // sync new board

        if (data.winner) {
            renderBoard(data.winning_combo || []); // highlight win
            statusEl.textContent =
                data.winner === "O" ? "You Win!" :
                data.winner === "X" ? "You Lose." :
                "It's a Draw!";
            isHumanTurn = false;
            gameOver = true;
            return
        } else {
            renderBoard(); // No winner yet, draw board
            statusEl.textContent = "Your Turn!";
            isHumanTurn = true;
        }
    });
}