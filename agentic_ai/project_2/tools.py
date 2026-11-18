import argparse
import json


TOPICS = {"loops": ["for", "while"], "functions": ["parameters", "return"]}


def lookup_topic(arguments):
    if set(arguments) != {"name"} or not isinstance(arguments["name"], str):
        raise ValueError("Expected a text name.")
    terms = TOPICS.get(arguments["name"].casefold())
    if terms is None:
        raise ValueError("Topic not found.")
    return {"terms": terms}


def estimate_time(arguments):
    if set(arguments) != {"pages"} or type(arguments["pages"]) is not int:
        raise ValueError("Expected an integer page count.")
    pages = arguments["pages"]
    if not 1 <= pages <= 100:
        raise ValueError("Use 1 to 100 pages.")
    return {"minutes": pages * 3}


TOOLS = {"lookup_topic": lookup_topic, "estimate_time": estimate_time}


def dispatch(name, arguments_json):
    if name not in TOOLS:
        raise ValueError("Unknown tool.")
    arguments = json.loads(arguments_json)
    if not isinstance(arguments, dict):
        raise ValueError("Expected a JSON object.")
    return TOOLS[name](arguments)


def main():
    parser = argparse.ArgumentParser(description="Run a structured study tool request.")
    parser.add_argument("tool")
    parser.add_argument("arguments")
    args = parser.parse_args()
    try:
        print(json.dumps(dispatch(args.tool, args.arguments)))
    except ValueError as error:
        parser.exit(1, f"Rejected request: {error}\n")


if __name__ == "__main__":
    main()
