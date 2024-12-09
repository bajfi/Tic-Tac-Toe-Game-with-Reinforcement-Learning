from typing import Dict

import numpy as np

from .state import State


def get_all_states_impl(
    current_state: State, current_symbol: int, all_states: Dict
) -> None:
    """Recursively generate all possible game states"""
    empty_positions = np.argwhere(current_state.data == 0)

    for i, j in empty_positions:
        new_state = current_state.next_state(i, j, current_symbol)
        new_hash = new_state.hash()

        if new_hash not in all_states:
            is_end = new_state.is_end()
            all_states[new_hash] = (new_state, is_end)
            if not is_end:
                get_all_states_impl(new_state, -current_symbol, all_states)


def get_all_states() -> Dict:
    """Generate dictionary of all possible game states"""
    current_state = State()
    all_states = {}
    all_states[current_state.hash()] = (current_state, current_state.is_end())
    get_all_states_impl(current_state, 1, all_states)
    return all_states


# Cache all possible states
all_states = get_all_states()
