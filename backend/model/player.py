import pickle
from collections import defaultdict
from typing import List, Optional

import numpy as np

from .constants import MODEL_DIR
from .state import State
from .state_utils import all_states


class Player:
    def __init__(self, step_size: float = 0.1, epsilon: float = 0.1):
        self.estimations = defaultdict(lambda: 0.5)
        self.step_size = step_size
        self.epsilon = epsilon
        self.states: List[State] = []
        self.greedy: List[bool] = []
        self.symbol = 0

    def reset(self) -> None:
        """Clear episode history"""
        self.states.clear()
        self.greedy.clear()

    def set_state(self, state: State) -> None:
        """Add state to episode history"""
        self.states.append(state)
        self.greedy.append(True)

    def set_symbol(self, symbol: int) -> None:
        """Initialize player with given symbol and setup initial state values"""
        self.symbol = symbol
        for hash_val, (state, is_end) in all_states.items():
            if is_end:
                if state.winner == self.symbol:
                    self.estimations[hash_val] = 1.0
                elif state.winner == 0:
                    self.estimations[hash_val] = 0.5
                else:
                    self.estimations[hash_val] = 0

    def backup(self) -> None:
        """Update state value estimates using TD learning"""
        states = [state.hash() for state in self.states]
        for i in range(len(states) - 2, -1, -1):
            td_error = self.greedy[i] * (
                self.estimations[states[i + 1]] - self.estimations[states[i]]
            )
            self.estimations[states[i]] += self.step_size * td_error

    def act(self) -> Optional[List]:
        """Choose action using epsilon-greedy policy"""
        state = self.states[-1]
        empty_positions = np.argwhere(state.data == 0)

        if len(empty_positions) == 0:
            return None

        next_states = [
            state.next_state(i, j, self.symbol).hash() for i, j in empty_positions
        ]

        if np.random.random() < self.epsilon:
            idx = np.random.randint(len(empty_positions))
            action = empty_positions[idx].tolist()
            self.greedy[-1] = False
        else:
            values = [
                (self.estimations[hash_val], pos)
                for hash_val, pos in zip(next_states, empty_positions)
            ]
            np.random.shuffle(values)
            action = max(values, key=lambda x: x[0])[1].tolist()

        action.append(self.symbol)
        return action

    def save_policy(self) -> None:
        """Save learned policy to file"""
        policy_file = (
            MODEL_DIR / f"policy_{'first' if self.symbol == 1 else 'second'}.bin"
        )
        with open(policy_file, "wb") as f:
            pickle.dump(dict(self.estimations), f)

    def load_policy(self) -> None:
        """Load policy from file"""
        policy_file = (
            MODEL_DIR / f"policy_{'first' if self.symbol == 1 else 'second'}.bin"
        )
        try:
            with open(policy_file, "rb") as f:
                self.estimations = defaultdict(lambda: 0.5, pickle.load(f))
        except FileNotFoundError:
            print(
                f"Warning: Policy file {policy_file} not found. Using default estimations."
            )
            self.estimations = defaultdict(lambda: 0.5)
