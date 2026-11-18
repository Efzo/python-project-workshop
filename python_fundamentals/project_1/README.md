# Project 1 — Quiz game

**Goal** Build a terminal quiz that asks three questions, counts correct answers and lets the player replay.

Run these commands from the `python_fundamentals` folder. Work through the files in order.

```sh
python3 project_1/01_first_program.py
python3 project_1/02_check_answer.py
python3 project_1/03_quiz.py
```

Type the commands in your terminal. When the running program asks a question, type your answer and press Enter. Press Ctrl+C if you need to stop a run early.

## 1. Ask for a name

In [01_first_program.py](01_first_program.py), `input(...)` prints a prompt and waits for Enter. It returns a string. `.strip()` removes surrounding whitespace, then `=` saves the result in the variable `name`. The `f` prefix lets Python substitute the value of `name` inside `{name}`.

Type `  Ada  ` and expect `Hello, Ada!`. Try removing `.strip()` and predict what will change.

## 2. Check one answer

In [02_check_answer.py](02_check_answer.py), `answer == "5"` evaluates to `True` or `False`. The quotes matter because `input()` gives you text. `5` is an integer, so `"5" == 5` is false. `=` assigns a value and `==` compares two values.

Python uses indentation to decide which statements belong to `if` and `else`. Run once with `5` and once with `4` to see both branches.

## 3. Turn it into a game

In [03_quiz.py](03_quiz.py), `questions` is a list. Each inner list contains the question and the expected answer in that order. In `for question, expected in questions`, Python unpacks one pair at a time into the two variables.

- `score` starts at zero inside the replay loop. `score += 1` assigns `score + 1` to it after a correct answer.
- `.lower()` lets an answer such as `PARIS` match `Paris`. Both sides of the comparison use the same rule.
- `len(questions)` counts the pairs. The percentage uses division and multiplication. In the f-string, `:.0f` displays the number rounded to zero decimal places.
- The inner `while` repeats only the replay prompt after invalid input. The outer `while True` starts another round until `break` runs.

Try the answers `5`, `IF`, and `London`. Expect `Score: 2/3 (67%)`. At the replay prompt, try `maybe`, then `y`. The quiz should prompt again after `maybe`, then start a fresh round after `y`. Get all three wrong in that second round and expect `Score: 0/3 (0%)`.

## Your turn

1. Add a fourth question. Check that three correct answers produce `Score: 3/4 (75%)`.
2. Add a message for a perfect score. Hint: compare `score` with `total` after the `for` loop. Check 4/4 and 3/4.
3. Show the question numbers. Start a counter at 1 before the `for` loop and increase it after every answer. Check that replay starts at 1 again.
4. Rebuild the game without the example open. Start with one question, then add the list, scoring and replay.

**Debugging challenge** Move `score = 0` above the outer loop. Play twice, with one correct answer each time, and explain why the second score is wrong. Restore the line once you can explain it.

Next up is [Project 2 — Expense tracker](../project_2/README.md).
