from typing import Tuple

from .state import BOARD_COLS, State


class HumanPlayer:
    def __init__(self, **kwargs):
        self.symbol = None
        self.keys = ["q", "w", "e", "a", "s", "d", "z", "x", "c"]
        self.state = None

    def reset(self) -> None:
        pass

    def set_state(self, state: State) -> None:
        self.state = state

    def set_symbol(self, symbol: int) -> None:
        self.symbol = symbol

    def act(self) -> Tuple[int, int, int]:
        """Get human player move input"""
        self.state.print_state()
        key = input("Input your position:")
        data = self.keys.index(key)
        i = data // BOARD_COLS
        j = data % BOARD_COLS
        return i, j, self.symbol
