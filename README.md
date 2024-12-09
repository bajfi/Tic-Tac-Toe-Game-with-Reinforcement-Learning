# Tic-Tac-Toe Game

A modern implementation of the classic Tic-Tac-Toe game with a web-based interface and AI opponent capabilities.

## Features

- Web-based user interface
- Player vs AI gameplay
- RESTful API backend
- Machine learning model for AI opponent

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd tic-tac-toe
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Install the package in development mode:

```bash
pip install -e .
```

## Usage

First, train the model:

```bash
python train_model.py
```

Then, start the game in development mode:

```bash
python run_dev.py
```

This will:

1. Start the Flask backend server
2. Automatically open your default web browser to <http://localhost:5000>
3. You can then play the game through the web interface

To stop the server, press `Ctrl+C` in the terminal.

## Project Structure

```
tic-tac-toe/
├── backend/           # Flask backend server
├── frontend/         # Web interface files
├── models/           # AI model implementations
├── tests/            # Test suite
├── requirements.txt  # Project dependencies
├── setup.py         # Package setup configuration
├── run_dev.py       # Development server launcher
└── train_model.py   # AI model training script
```

## Development

The project uses several development tools:

- `ruff` for code linting
- `pre-commit` for git hooks
- Flask for the backend server
- Flask-CORS for handling cross-origin requests

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues or have questions, please file an issue in the project's issue tracker.
