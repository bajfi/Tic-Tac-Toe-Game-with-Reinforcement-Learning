from typing import Optional

import numpy as np
from numpy.typing import NDArray

# Board dimensions
BOARD_ROWS = 3
BOARD_COLS = 3
BOARD_SIZE = BOARD_ROWS * BOARD_COLS


class State:
    def __init__(self):
        # Board representation: 0=empty, 1=player1, -1=player2
        self.data: NDArray = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=np.int32)
        self.winner: Optional[int] = None
        self.hash_val: Optional[int] = None
        self.end: Optional[bool] = None

    def hash(self) -> int:
        """Compute unique hash value for board state using base-3 encoding"""
        if self.hash_val is None:
            flat_board = self.data.ravel() + 1  # Shift values to [0,1,2]
            powers = 3 ** np.arange(BOARD_SIZE)
            self.hash_val = np.sum(flat_board * powers)
        return self.hash_val

    def is_end(self) -> bool:
        """Check if game has ended (win/loss/draw)"""
        if self.end is not None:
            return self.end

        row_sums = np.sum(self.data, axis=1)
        col_sums = np.sum(self.data, axis=0)
        diag_sum = np.trace(self.data)
        anti_diag_sum = np.trace(np.fliplr(self.data))

        all_sums = np.concatenate([row_sums, col_sums, [diag_sum, anti_diag_sum]])

        if 3 in all_sums:
            self.winner = 1
            self.end = True
            return True
        if -3 in all_sums:
            self.winner = -1
            self.end = True
            return True

        if np.sum(np.abs(self.data)) == BOARD_SIZE:
            self.winner = 0
            self.end = True
            return True

        self.end = False
        return False

    def next_state(self, i: int, j: int, symbol: int) -> "State":
        """Generate next state after placing symbol at position (i,j)"""
        new_state = State()
        new_state.data = self.data.copy()
        new_state.data[i, j] = symbol
        return new_state

    def print_state(self) -> None:
        """Display current board state"""
        symbols = {0: "0", 1: "*", -1: "x"}
        print("-------------")
        for row in self.data:
            print("| " + " | ".join(symbols[x] for x in row) + " |")
            print("-------------")
