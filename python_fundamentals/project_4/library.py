from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    code: str
    title: str


class Library:
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.checked_out: set[str] = set()

    def add(self, book: Book) -> None:
        if book.code in self.books:
            raise ValueError(f"Book {book.code} is already registered.")
        self.books[book.code] = book

    def check_out(self, code: str) -> None:
        if code not in self.books:
            raise ValueError(f"Unknown book: {code}")
        if code in self.checked_out:
            raise ValueError(f"Book {code} is already on loan.")
        self.checked_out.add(code)

    def return_book(self, code: str) -> None:
        if code not in self.checked_out:
            raise ValueError(f"Book {code} is not on loan.")
        self.checked_out.remove(code)

    def available(self) -> list[Book]:
        return [book for code, book in self.books.items() if code not in self.checked_out]


def main() -> None:
    library = Library()
    library.add(Book("B01", "The Hobbit"))
    library.add(Book("B02", "Pride and Prejudice"))
    library.check_out("B01")
    print("Available during loan:", [book.title for book in library.available()])
    library.return_book("B01")
    print("Available after return:", [book.title for book in library.available()])


if __name__ == "__main__":
    main()
