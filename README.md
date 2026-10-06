# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Purpose:** a Streamlit number-guessing game. You pick a difficulty, guess the secret number within a limited number of attempts, get Higher/Lower hints, and earn a score.
- [x] **Bugs found:**
  - Hints were backwards ("Too High" told you to go higher).
  - On every even attempt the secret was converted to a string, so a correct guess could never win and comparisons like `"9" > "50"` gave wrong hints.
  - "New Game" did not reset status, score or history, and ignored the difficulty range.
  - The attempts counter started at 1 (off by one), the prompt always said "1 to 100", Hard (1-50) was easier than Normal, and "Too High" could add points.
- [x] **Fixes applied:**
  - Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` into `logic_utils.py` and fixed them (correct hints, int-only comparison, Hard = 1-200, wrong guesses always cost 5 points).
  - `app.py` now imports from `logic_utils`, starts attempts at 0, uses one `reset_game()` for New Game and difficulty changes, shows the real range, and no longer counts invalid input as an attempt.
  - Added pytest regression tests in `tests/test_game_logic.py`.

## 📸 Demo Walkthrough

1. Start on Normal difficulty (range 1-100, 8 attempts). The debug panel shows the secret is 63.
2. The player enters 40 and the game answers "📈 Go HIGHER!" (the hint is now correct).
3. The score drops to -5 for the wrong guess.
4. The player enters 63 on attempt 2. Previously an even attempt could never win. Now the game shows "🎉 Correct!" and "You won! The secret was 63. Final score: 85" (-5, then +90 for winning on attempt 2).
5. Clicking "New Game" resets attempts to 0, score to 0 and history to empty, and picks a new secret (23).
6. Switching to Hard now shows a wider range (1-200) and starts a fresh game.

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\rsung\AI110\ai110-module1show-gameglitchinvestigator-starter\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\rsung\AI110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collecting ... collected 10 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 10%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 20%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 30%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 40%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 50%]
tests/test_game_logic.py::test_numeric_comparison_not_string PASSED      [ 60%]
tests/test_game_logic.py::test_parse_guess_valid_and_invalid PASSED      [ 70%]
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED    [ 80%]
tests/test_game_logic.py::test_wrong_guess_never_increases_score PASSED  [ 90%]
tests/test_game_logic.py::test_win_score_has_floor PASSED                [100%]

============================= 10 passed in 0.05s ==============================
```

## 🚀 Stretch Features

- [ ] No stretch challenges were completed.
