# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The game loaded as a normal Streamlit number guesser with difficulty settings, a guess box, and a debug expander. Playing it showed that the hints pointed the wrong way, that every second guess could never win even when I typed the secret number, and that "New Game" did not actually restart a finished game. The starter tests also failed because `logic_utils.py` was only stubs.

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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used Claude Code (agent mode) in the Claude desktop app.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Claude pointed out that `app.py` converted the secret to `str(secret)` on every even attempt, which is why a correct guess could never win, and suggested deleting that toggle and comparing ints only. I accepted it because it explained the "can't win" symptom exactly. I verified it with a regression test (`test_numeric_comparison_not_string`) and in the live game: guessing the secret 63 on attempt 2 (an even attempt) now shows "Correct!" and a win.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  A fuller rewrite of `parse_guess` was considered, with range checks, negative-number handling and a custom error type. I kept the small version (strip whitespace, reject blanks and non-numbers) because the assignment is about fixing the existing bugs and the extra validation would have made the function harder to read and was out of scope. I verified the simple version with `test_parse_guess_valid_and_invalid`.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  A bug counted as fixed when I had both a failing-then-passing test and a matching check in the running game. For example, the hints were fixed when `check_guess(60, 50)` returned a message containing "LOWER" and the app told me to go higher for a guess of 40 against a secret of 63.
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  The starter tests initially failed with `NotImplementedError` because `logic_utils.py` was only stubs. They also compared the whole `(outcome, message)` tuple to a string, so I changed them to unpack the outcome. After the fixes, `python -m pytest -v` shows 10 passed (see `test_results.txt` and the README). In the live app I played a low guess, then the winning guess (score 85), then New Game, which reset everything.
- Did AI help you design or understand any tests? How?
  Yes. Claude suggested the regression tests that target each bug (backwards hints, str-vs-int comparison, score never rising on a wrong guess, Hard being wider than Normal), and I reviewed each assertion to make sure it checked real behavior.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Streamlit re-runs the whole script from top to bottom every time you click a button or type something, so normal variables reset each time. `st.session_state` is a dictionary that survives those reruns, so anything that has to persist (the secret number, attempts, score) must be stored there. The original game's trouble with New Game came from not resetting all of that state together.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  Writing a small regression test for each bug before trusting the fix, and committing in separate steps (log, fix, docs).
- What is one thing you would do differently next time you work with AI on a coding task?
  I would read the AI's diff more slowly and ask it to explain each change, instead of just checking that the app runs.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  AI code can look polished and still hide logic bugs, like the string-converted secret, so it needs tests and human review. The AI is most useful when I give it a specific bug and then check its work myself.
