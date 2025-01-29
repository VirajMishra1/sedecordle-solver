# Sedecordle Solver - Multi-Game Entropy Assistant 🧩×16

## Project Description

The **Sedecordle Solver** is a Python-based tool designed to solve 16 simultaneous Wordle puzzles (Sedecordle). Using entropy-driven calculations and parallel game state management, it recommends optimal guesses that maximize information gain across all active games. The tool handles complex constraints from multiple feedback streams and narrows down solutions efficiently.

## 🚀 Features

1. **16-Game Parallel Management**: Tracks and updates constraints for 16 simultaneous Wordle games.
2. **Aggregate Entropy Scoring**: Prioritizes guesses that maximize information gain across all active games.
3. **Dynamic Feedback Handling**: Processes per-game feedback (C/P/A) and marks solved games automatically.
4. **Batch Input Support**: Streamlines feedback entry for multiple active games in a single attempt.
5. **Smart Constraint Resolution**: Automatically cleans conflicting letter constraints across games.
6. **Progress Visualization**: Displays remaining possibilities for each active game and total solved count.

## 🛠️ Technologies Used

- **Python**: Core programming language.
- **tqdm**: For progress bars during entropy calculations.
- **Defaultdict**: Efficient pattern caching and word list management.

## 📦 Setup and Installation

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd sedecordle-solver
    ```
3. **Install Dependencies**:
    ```bash
    pip install tqdm
    ```
4. **Prepare Word Lists**:
   - Obtain two text files:
     - `wordle_answers.txt`: Valid answer words (one 5-letter word per line).
     - `wordle_guesses.txt`: Allowed guess words (optional; uses answers if omitted).
   - Update paths in the `main()` function:
     ```python
     answer_path="/path/to/your/wordle_answers.txt"
     guess_path="/path/to/your/wordle_guesses.txt"
     ```

5. **Run the Solver**:
    ```bash
    python sedecordle_solver.py
    ```

## 📝 Usage

1. **Initialize the Solver**:
   - The tool loads word lists and initializes 16 parallel game states.

2. **Follow Interactive Prompts**:
   - After each recommended guess:
     - Enter feedback for **active games** using `C/P/A` (e.g., `CPAAP`).
     - Type `SOLVED` to mark a completed game.
   - Example workflow:
     ```
     NEXT GUESS: CRANE
     Provide feedback for 12 active game(s):
     [Game 3/12] Feedback: CCAPA
     [Game 7/12] Feedback: SOLVED
     ```

3. **Track Progress**:
   - The solver displays remaining possible words per game and updates solved counts after each attempt.

## 🛡️ Notes

- **Performance**: Initial entropy calculations may take longer due to 16-game complexity. Candidate limiting (`candidates = self.allowed[:2316]`) balances speed/accuracy.
- **Word List Compatibility**: Uses standard Wordle answer/guess lists. Ensure files contain valid 5-letter words.
- **Feedback Precision**: Provide feedback **only for active games** to avoid mismatches.

## 🤝 Contribution

Contributions are welcome! Potential improvements:
- Optimize multi-game entropy calculations
- Add GUI for batch feedback input
- Implement auto-constraint propagation between games

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Viraj Mishra
