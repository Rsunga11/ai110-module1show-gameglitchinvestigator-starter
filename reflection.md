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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
