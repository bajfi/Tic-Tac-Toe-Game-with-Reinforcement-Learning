#!/usr/bin/env python3
"""Training script for Tic-Tac-Toe AI model."""

from backend.model.constants import MODEL_DIR
from backend.model.train import train


def main():
    """Run the training process."""
    print("Starting training...")
    train(100_000)  # Train for 100,000 episodes
    print(
        f"Training complete. Models saved to:\n"
        f"  - {MODEL_DIR / 'policy_first.bin'}\n"
        f"  - {MODEL_DIR / 'policy_second.bin'}"
    )


if __name__ == "__main__":
    main()
