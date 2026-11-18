import unittest

from library import Book, Library


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book = Book("B01", "The Hobbit")
        self.library.add(self.book)

    def test_check_out_and_return(self):
        self.library.check_out("B01")
        self.assertEqual(self.library.available(), [])
        self.library.return_book("B01")
        self.assertEqual(self.library.available(), [self.book])

    def test_cannot_check_out_same_book_twice(self):
        self.library.check_out("B01")
        with self.assertRaisesRegex(ValueError, "already on loan"):
            self.library.check_out("B01")

    def test_cannot_register_same_code_twice(self):
        with self.assertRaisesRegex(ValueError, "already registered"):
            self.library.add(Book("B01", "Another title"))


if __name__ == "__main__":
    unittest.main()
