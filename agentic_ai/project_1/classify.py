import argparse
from dataclasses import dataclass
import json
import re


INSTRUCTIONS = "Classify the request as study, planning, or other. Return category and reason."
CATEGORIES = {"study", "planning", "other"}


@dataclass(frozen=True)
class Classification:
    category: str
    reason: str


class FixtureModel:
    def complete(self, instructions, text):
        if instructions != INSTRUCTIONS:
            raise ValueError("This fixture handles the classification prompt only.")
        words = set(re.findall(r"\w+", text.casefold()))
        if words & {"study", "learn", "review"}:
            category = "study"
        elif words & {"plan", "schedule", "organize"}:
            category = "planning"
        else:
            category = "other"
        return json.dumps({"category": category, "reason": "Matched fixture vocabulary."})


def classify(model, text):
    data = json.loads(model.complete(INSTRUCTIONS, text))
    if not isinstance(data, dict) or set(data) != {"category", "reason"}:
        raise ValueError("Expected an object with category and reason.")
    category = data["category"]
    reason = data["reason"]
    if not isinstance(category, str) or category not in CATEGORIES:
        raise ValueError("Unexpected category.")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Expected a reason.")
    return Classification(category, reason)


def main():
    parser = argparse.ArgumentParser(description="Classify a request with a local fixture.")
    parser.add_argument("text")
    args = parser.parse_args()
    result = classify(FixtureModel(), args.text)
    print(f"{result.category} — {result.reason}")


if __name__ == "__main__":
    main()
