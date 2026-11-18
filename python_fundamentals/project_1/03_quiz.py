questions = [
    ["What is 2 + 3?", "5"],
    ["What keyword starts a conditional in Python?", "if"],
    ["What is the capital of France?", "Paris"],
]

while True:
    score = 0

    for question, expected in questions:
        answer = input(f"{question} ").strip().lower()
        if answer == expected.lower():
            score += 1
            print("Correct!")
        else:
            print(f"The answer is {expected}.")

    total = len(questions)
    percentage = score / total * 100
    print(f"Score: {score}/{total} ({percentage:.0f}%)")

    replay = input("Play again? [y/n] ").strip().lower()
    while replay not in ["y", "n"]:
        replay = input("Please enter y or n: ").strip().lower()
    if replay == "n":
        break

print("Thanks for playing!")
