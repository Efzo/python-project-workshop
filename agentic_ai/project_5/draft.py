import argparse
from pathlib import Path


TOPICS = {"loops": "Write a for loop over a list.", "files": "Read a text file with a with block."}


def propose(topic):
    exercise = TOPICS.get(topic.casefold().strip())
    if exercise is None:
        raise ValueError("No exercise is available for this topic.")
    return f"Study exercise\n\n{exercise}\n"


def run(topic, directory, approved):
    text = propose(topic)
    if not approved:
        return f"Draft preview (approval required to save)\n\n{text}"

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "exercise.txt"
    with path.open("x", encoding="utf-8") as file:
        file.write(text)
    return f"Saved {path}"


def main():
    parser = argparse.ArgumentParser(description="Preview a study exercise before saving it.")
    parser.add_argument("topic")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args()
    try:
        print(run(args.topic, args.output_dir, args.approve))
    except (ValueError, OSError) as error:
        parser.exit(1, f"Could not finish draft: {error}\n")


if __name__ == "__main__":
    main()
