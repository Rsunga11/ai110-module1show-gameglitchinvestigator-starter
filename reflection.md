# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game it looked like a normal Streamlit number guesser, but it did not behave like one. The hints pointed the wrong way, every second guess could not win even when I entered the secret from the debug panel, and "New Game" did not restart a finished game. The starter tests also failed because `logic_utils.py` only contained stubs.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret is 50, guess 60 | "Too High" hint tells me to go lower | Shows "📈 Go HIGHER!" (and "Go LOWER!" for a low guess) | No error; hint text is simply backwards (`check_guess`, app.py) |
| Secret is 50, guess 50 on an even-numbered attempt (2nd, 4th...) | "Win" | No win; hint says Too Low/High. App passes `str(secret)` on even attempts so `50 == "50"` is False | No error; `TypeError` fallback silently compares strings (`"9" > "50"` is True) |
| Win or run out of attempts, then click "New Game" | Fresh game: score, history, status reset | Still shows "You already won / Game over"; score and history persist; new secret always 1-100 | No error; `status` is never reset to "playing" |
| Switch difficulty to Hard | Harder than Normal | Range is 1-50 (smaller than Normal's 1-100); prompt text still says "between 1 and 100" | None |
| `pytest` on starter code | Starter tests pass | 3 failed | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

- **Tool:** I used Claude Code (in the Claude desktop app) for this project.
- **A suggestion that was correct:** Claude found that `app.py` turned the secret into a string (`str(secret)`) on every even attempt, which is why a correct guess never won, and suggested removing that toggle and comparing integers only. That matched the symptom exactly, so I accepted it. I checked it with the regression test `test_numeric_comparison_not_string` and in the live game, where guessing the secret (63) on attempt 2 now shows "Correct!" and a win.
- **A suggestion I did not accept as written:** A larger rewrite of `parse_guess` was an option, with range checks, negative-number handling and a custom error type. I kept the small version (strip whitespace, reject blank or non-numeric input) because the assignment is about fixing the bugs that were there, and the extra validation made the function harder to read and was out of scope. I checked the simple version with `test_parse_guess_valid_and_invalid`.
- **How much AI did:** Claude Code wrote most of the code changes in agent mode, and I reviewed the diffs and ran the tests and the app to confirm the fixes. I'm noting that plainly because the work was AI-driven rather than something I wrote line by line.

---

## 3. Debugging and testing your fixes

- **How I decided a bug was fixed:** A bug counted as fixed when a test covered it and the running game agreed. For example, the hint bug was fixed when `check_guess(60, 50)` returned a message containing "LOWER", and the app told me to go higher for a guess of 40 against a secret of 63.
- **A test I ran:** The starter tests first failed with `NotImplementedError`, and they also compared the whole `(outcome, message)` tuple to a string, so they were updated to unpack the outcome. After the fixes, `python -m pytest -v` shows 10 passed (see `test_results.txt` and the README). In the live app I made a wrong guess, then the winning guess (score 85), then clicked New Game, which reset attempts, score and history.
- **AI and tests:** Yes. Claude suggested regression tests aimed at each bug (backwards hints, string vs. integer comparison, wrong guesses never adding points, Hard being wider than Normal), and I read each assertion to make sure it checked real behavior.

---

## 4. What did you learn about Streamlit and state?

- Streamlit re-runs the whole script from top to bottom every time you click a button or type in a box, so ordinary variables reset on each run. `st.session_state` is a dictionary that survives those reruns, so anything that has to persist (the secret, attempts, score, status, history) has to live there. The original New Game bug came from only resetting some of that state instead of all of it.

---

## 5. Looking ahead: your developer habits

- **A habit to reuse:** Writing a small regression test for each bug before trusting a fix, and committing in separate steps (bug log, fixes, docs).
- **What I'd do differently:** I would work through each fix myself first and use AI to check my work, instead of letting it make the changes, so I understand every line.
- **How my view changed:** AI-generated code can look polished and still hide logic bugs, like the string-converted secret, so it needs tests and human review.
