# Import required libraries (same as Wordle solver)
import math
from collections import defaultdict
from tqdm import tqdm  # For progress visualization

class SedecordleSolver:
    _pattern_cache = {}  # Class-level cache for pattern calculations
    
    def __init__(self, answer_path, guess_path=None):
        # Initialize with answer words and allowed guesses
        self.answers = self.load_valid_words(answer_path)
        self.allowed = self.load_valid_words(guess_path) if guess_path else self.answers.copy()
        
        # Print loading statistics
        print(f"Loaded {len(self.answers)} answer words")
        print(f"Loaded {len(self.allowed)} allowed guesses")
        
        # Initialize 16 independent game states
        self.games = [{
            'possible': self.answers.copy(),  # Possible solutions for each game
            'correct': ['?'] * 5,  # Known correct positions
            'present': set(),  # Present letters (wrong position)
            'absent': set()  # Excluded letters
        } for _ in range(16)]  # Create 16 copies for 16 simultaneous games

    def load_valid_words(self, file_path):
        # Load and validate 5-letter words from file
        try:
            with open(file_path, 'r') as f:
                words = [word.strip().upper() for word in f if len(word.strip()) == 5]
                if not words:
                    print(f"Error: No valid 5-letter words found in '{file_path}'!")
                    exit(1)
                return words
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found!")
            exit(1)

    # Pattern calculation methods identical to Wordle solver
    @staticmethod
    def get_pattern(guess, target):
        # Calculate Wordle feedback pattern (C=Correct, P=Present, A=Absent)
        pattern = [''] * 5
        counts = defaultdict(int)
        
        # First pass: Mark correct letters
        for i, (g, t) in enumerate(zip(guess, target)):
            if g == t:
                pattern[i] = 'C'
                counts[t] += 1
        
        # Second pass: Handle present/absent letters
        for i, g in enumerate(guess):
            if pattern[i] == 'C':
                continue
            
            total_in_target = sum(1 for t in target if t == g)
            if total_in_target > counts[g]:
                pattern[i] = 'P'
                counts[g] += 1
            else:
                pattern[i] = 'A'
        
        return tuple(pattern)

    @staticmethod
    def get_pattern_cached(guess, target):
        # Memoized version of get_pattern for performance
        key = (guess, target)
        if key not in SedecordleSolver._pattern_cache:
            SedecordleSolver._pattern_cache[key] = SedecordleSolver.get_pattern(guess, target)
        return SedecordleSolver._pattern_cache[key]

    def calculate_entropy(self, word, game_states):
        # Calculate combined entropy across all active games
        total_entropy = 0
        for state in game_states:
            if not state['possible']:
                continue  # Skip solved games
                
            pattern_counts = defaultdict(int)
            # Count patterns for all possible answers in this game
            for possible in state['possible']:
                pattern = self.get_pattern_cached(word, possible)
                pattern_counts[pattern] += 1
            
            # Calculate entropy for this game and add to total
            total = len(state['possible'])
            entropy = sum(-(count/total) * math.log2(count/total) 
                        for count in pattern_counts.values())
            total_entropy += entropy
        
        return total_entropy

    def get_best_guess(self):
        # Find optimal guess that maximizes information across all active games
        active_games = [g for g in self.games if g['possible']]
        if not active_games:
            return None  # All games solved
        
        best_word = None
        best_score = -float('inf')
        
        # Optimization: Limit candidate words for initial guesses
        print("\nCalculating best initial guess...")
        candidates = self.allowed[:2316]  # Standard Wordle answer list size
        
        # Analyze candidates with progress visualization
        for word in tqdm(candidates, desc="Analyzing words"):
            score = self.calculate_entropy(word, active_games)
            if score > best_score:
                best_score = score
                best_word = word
                tqdm.write(f"Current best: {word} ({score:.2f})")  # Live updates
        
        return best_word

    def update_games(self, guess, feedbacks):
        # Update all games based on their individual feedback
        for game_idx, feedback in enumerate(feedbacks):
            if not feedback:
                continue  # No feedback for this game
                
            game = self.games[game_idx]
            new_possible = []
            
            # Update game state from feedback
            for i, (letter, color) in enumerate(feedback):
                if color == 'C':
                    game['correct'][i] = letter
                    if letter in game['present']:
                        game['present'].remove(letter)
                elif color == 'P':
                    game['present'].add(letter)
                elif color == 'A':
                    game['absent'].add(letter)
            
            # Filter possible words using updated constraints
            for word in game['possible']:
                valid = True
                
                # Check correct positions
                for i, c in enumerate(game['correct']):
                    if c != '?' and word[i] != c:
                        valid = False
                        break
                
                # Check required present letters
                if valid and any(p not in word for p in game['present']):
                    valid = False
                
                # Check excluded letters
                if valid and any(a in word for a in game['absent'] 
                               if a not in game['correct'] and a not in game['present']):
                    valid = False
                
                # Prevent present letters in known incorrect positions
                if valid:
                    for i, letter in enumerate(word):
                        if letter in game['present'] and letter == game['correct'][i]:
                            valid = False
                            break
                
                if valid:
                    new_possible.append(word)
            
            game['possible'] = new_possible

    def clean_constraints(self):
        # Remove redundant constraints across all games
        for game in self.games:
            game['present'] = {p for p in game['present'] if p not in game['correct']}
            game['absent'] = {a for a in game['absent'] 
                            if a not in game['correct'] and a not in game['present']}

    def print_status(self):
        # Display status for all active games
        print("\nCurrent Game Status:")
        active_count = 0
        for i, game in enumerate(self.games):
            if game['possible']:
                active_count += 1
                status = f"Game {i+1:2}: {len(game['possible']):4} possible"
                if len(game['possible']) <= 3:
                    status += f" ({', '.join(game['possible'])})"
                print(status)
        print(f"Remaining games: {active_count}/16")

def get_feedback_input(guess, game_num, total_remaining, current):
    # Get and validate user feedback for each active game
    while True:
        print(f"\n{' INPUT REQUIRED ':~^60}")
        print(f"Game {game_num} ({current} of {total_remaining} remaining)".center(60))
        print(f"Current Guess: {guess}")
        print("Enter feedback using C/P/A for each letter:")
        print("Example: CPAAP or C P A A P")
        print("(C=Correct, P=Present, A=Absent, SOLVED=Game completed)")
        print(f"{'-'*60}")
        
        fb = input(">>> Feedback for this game: ").upper().replace(" ", "")
        
        if fb == "SOLVED":
            return None  # Mark game as completed
        if len(fb) == 5 and all(c in 'CPA' for c in fb):
            return list(zip(guess, fb))
        print("Invalid input! Please use exactly 5 characters (C/P/A)")

def main():
    # Initialize solver with word lists
    solver = SedecordleSolver(
        answer_path="filepath",
        guess_path="filepath"
    )
    
    # Print welcome banner
    print("\n" + "=" * 60)
    print(" SEDECORDLE SOLVER ".center(60, '='))
    print("=" * 60)
    print("NOTE: Provide feedback for ACTIVE games only".center(60))
    print("=" * 60)
    
    # Main game loop (max 21 attempts)
    for attempt in range(21):
        print(f"\n{' ATTEMPT ' + str(attempt+1) + ' ':=^60}")
        solver.print_status()
        
        # Get and display best guess
        best_guess = solver.get_best_guess()
        if not best_guess:
            print("\nALL GAMES SOLVED!")
            break
        
        print(f"\nNEXT GUESS: {best_guess}")
        print("Enter this word in ALL active games, then provide feedback:")
        
        # Collect feedback for active games
        active_games = [i for i, g in enumerate(solver.games) if g['possible']]
        all_feedbacks = [[] for _ in range(16)]
        
        if active_games:
            print(f"\nProvide feedback for {len(active_games)} active game(s):")
            for idx, game_idx in enumerate(active_games, 1):
                feedback = get_feedback_input(best_guess, game_idx+1, len(active_games), idx)
                
                if feedback is None:
                    # Mark game as solved by clearing possible words
                    solver.games[game_idx]['possible'] = []
                else:
                    all_feedbacks[game_idx] = feedback
        
        # Update game states and check completion
        solver.update_games(best_guess, all_feedbacks)
        solver.clean_constraints()
        
        if all(not game['possible'] for game in solver.games):
            print("\nCONGRATULATIONS! ALL GAMES SOLVED!")
            break

if __name__ == "__main__":
    main()