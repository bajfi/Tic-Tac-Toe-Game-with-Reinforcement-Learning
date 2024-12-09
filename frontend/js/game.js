class TicTacToe {
  constructor() {
    this.board = Array(9).fill("");
    this.currentPlayer = "X";
    this.gameActive = true;
    this.cells = document.querySelectorAll(".cell");
    this.statusDisplay = document.querySelector(".game-status");
    this.resetButton = document.querySelector(".reset-button");

    this.initializeGame();
  }

  initializeGame() {
    this.cells.forEach((cell) => {
      cell.addEventListener("click", () => this.handleCellClick(cell));
    });

    this.resetButton.addEventListener("click", () => this.resetGame());
  }

  handleCellClick(cell) {
    const index = cell.getAttribute("data-index");

    if (this.board[index] === "" && this.gameActive) {
      this.board[index] = this.currentPlayer;
      cell.classList.add(this.currentPlayer.toLowerCase());

      if (this.checkWin()) {
        this.statusDisplay.textContent = `🎉 Player ${this.currentPlayer} wins! 🎉`;
        this.gameActive = false;
        return;
      }

      if (this.checkDraw()) {
        this.statusDisplay.textContent = "🤝 Game ended in a draw! 🤝";
        this.gameActive = false;
        return;
      }

      this.currentPlayer = this.currentPlayer === "X" ? "O" : "X";
      this.statusDisplay.textContent = `Player ${this.currentPlayer}'s turn 🎮`;

      if (this.currentPlayer === "O") {
        this.getAIMove();
      }
    }
  }

  async getAIMove() {
    try {
      const response = await fetch("/api/move", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ board: this.board }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      const aiMove = data.move;

      // Apply AI's move
      if (this.board[aiMove] === "") {
        this.board[aiMove] = this.currentPlayer;
        this.cells[aiMove].classList.add(this.currentPlayer.toLowerCase());

        if (this.checkWin()) {
          this.statusDisplay.textContent = `🎉 Player ${this.currentPlayer} wins! 🎉`;
          this.gameActive = false;
          return;
        }

        if (this.checkDraw()) {
          this.statusDisplay.textContent = "🤝 Game ended in a draw! 🤝";
          this.gameActive = false;
          return;
        }

        this.currentPlayer = "X";
        this.statusDisplay.textContent = `Player ${this.currentPlayer}'s turn 🎮`;
      }
    } catch (error) {
      console.error("Error getting AI move:", error);
    }
  }

  checkWin() {
    const winPatterns = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8], // Rows
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8], // Columns
      [0, 4, 8],
      [2, 4, 6], // Diagonals
    ];

    return winPatterns.some((pattern) => {
      const [a, b, c] = pattern;
      return (
        this.board[a] &&
        this.board[a] === this.board[b] &&
        this.board[a] === this.board[c]
      );
    });
  }

  checkDraw() {
    return !this.board.includes("");
  }

  resetGame() {
    this.board = Array(9).fill("");
    this.currentPlayer = "X";
    this.gameActive = true;
    this.cells.forEach((cell) => {
      cell.classList.remove("x", "o");
    });
    this.statusDisplay.textContent = `Player ${this.currentPlayer}'s turn 🎮`;
  }
}

// Initialize the game when the page loads
document.addEventListener("DOMContentLoaded", () => {
  new TicTacToe();
});
