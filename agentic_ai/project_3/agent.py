import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    name: str
    value: str


@dataclass(frozen=True)
class Final:
    text: str


def fixture_model(question, observations):
    if not observations:
        if "loop" not in question.casefold():
            return Final("Try asking for a study plan about loops.")
        return Action("read_topic", "loops")
    if len(observations) == 1:
        return Action("estimate_minutes", observations[-1]["pages"])
    return Final(f"Study {observations[0]['title']} for {observations[-1]['minutes']} minutes.")


def dispatch(action):
    if action == Action("read_topic", "loops"):
        return {"title": "Python loops", "pages": "8"}
    if action.name == "estimate_minutes" and action.value in {"4", "8"}:
        return {"minutes": int(action.value) * 3}
    raise ValueError("Unsupported action or value.")


def run_agent(question, model=fixture_model, max_turns=4):
    observations = []
    for _ in range(max_turns):
        decision = model(question, observations)
        if isinstance(decision, Final):
            return decision.text
        if not isinstance(decision, Action):
            raise ValueError("Expected Action or Final.")
        observation = dispatch(decision)
        print(f"Tool {decision.name} -> {observation}")
        observations.append(observation)
    raise RuntimeError("Agent reached its turn limit before producing an answer.")


def main():
    parser = argparse.ArgumentParser(description="Trace a multi-step local agent.")
    parser.add_argument("question")
    parser.add_argument("--max-turns", type=int, choices=range(1, 6), default=4)
    args = parser.parse_args()
    try:
        print(run_agent(args.question, max_turns=args.max_turns))
    except (RuntimeError, ValueError) as error:
        parser.exit(1, f"Agent stopped: {error}\n")


if __name__ == "__main__":
    main()
