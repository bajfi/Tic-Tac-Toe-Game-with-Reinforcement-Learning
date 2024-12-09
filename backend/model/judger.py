from typing import Generator

from .state import State
from .state_utils import all_states


class Judger:
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.p1_symbol = 1
        self.p2_symbol = -1
        self.p1.set_symbol(self.p1_symbol)
        self.p2.set_symbol(self.p2_symbol)

    def reset(self) -> None:
        """Reset both players"""
        self.p1.reset()
        self.p2.reset()

    def alternate(self) -> Generator:
        """Generator to alternate between players"""
        while True:
            yield self.p1
            yield self.p2

    def play(self, print_state: bool = False) -> int:
        """Play a game between two players"""
        alternator = self.alternate()
        self.reset()
        current_state = State()

        self.p1.set_state(current_state)
        self.p2.set_state(current_state)

        if print_state:
            current_state.print_state()

        while True:
            player = next(alternator)
            i, j, symbol = player.act()
            next_state_hash = current_state.next_state(i, j, symbol).hash()
            current_state, is_end = all_states[next_state_hash]

            self.p1.set_state(current_state)
            self.p2.set_state(current_state)

            if print_state:
                current_state.print_state()

            if is_end:
                return current_state.winner
