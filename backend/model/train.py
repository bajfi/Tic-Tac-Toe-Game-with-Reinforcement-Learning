import numpy as np

from .judger import Judger
from .player import Player


def train(epochs: int, print_every_n: int = 500) -> None:
    """Train two AI players against each other"""
    player1 = Player(epsilon=0.01)
    player2 = Player(epsilon=0.01)
    judger = Judger(player1, player2)

    wins = np.zeros(2)  # Track wins efficiently

    for i in range(1, epochs + 1):
        winner = judger.play()
        if winner == 1:
            wins[0] += 1
        elif winner == -1:
            wins[1] += 1

        if i % print_every_n == 0:
            print(
                f"Epoch {i}, player 1 winrate: {wins[0]/i:.2f}, player 2 winrate: {wins[1]/i:.2f}"
            )

        player1.backup()
        player2.backup()
        judger.reset()

    player1.save_policy()
    player2.save_policy()


if __name__ == "__main__":
    train(100_000)
