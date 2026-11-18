import re


NOTES = {
    "loops": "Use a for loop to visit each item in a collection. Practice by counting even numbers.",
    "functions": "A function takes arguments and can return a value. Practice by writing a function that totals a list.",
    "sqlite": "SQLite stores data in a local database file. Practice inserting and selecting records with placeholders.",
}


def words(text):
    return set(re.findall(r"\w+", text.casefold()))


def call_tool(name, arguments):
    if not isinstance(arguments, dict):
        raise ValueError("Expected a JSON object.")
    if name == "search_notes" and set(arguments) == {"query"}:
        query = arguments["query"]
        if isinstance(query, str) and 0 < len(query) <= 500:
            query_words = words(query)
            return {"ids": [key for key in NOTES if key in query_words or key.rstrip("s") in query_words]}
    if name == "read_note" and set(arguments) == {"note_id"}:
        note_id = arguments["note_id"]
        if isinstance(note_id, str) and note_id in NOTES:
            return {"id": note_id, "text": NOTES[note_id]}
    raise ValueError("Unknown tool or invalid arguments.")
