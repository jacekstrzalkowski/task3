import unittest
from project import db
from project.books.models import Book


# Testy poprawnych danych
# Testy niepoprawnych danych
# Testy związane z próbą wstrzyknięcia kodu SQL i kodu JavaScript
# Testy ekstremalne


class BookModelTestCase(unittest.TestCase):

    # test poprawnych danych

    correct_inputs = {
        "name": "Test Book",
        "author": "Test Author",
        "year_published": 2021,
        "book_type": "Fiction",
    }

    def test_book_creation(self):

        book = Book(**self.correct_inputs)

        self.assertEqual(book.name, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year_published, 2021)
        self.assertEqual(book.book_type, "Fiction")

    # test niepoprawnych danych

    incorrect_inputs = {
        "name": "77771112331131#$",
        "author": "77771112331131#$",
        "year_published": "NOTAYEAR",
        "book_type": "163874",
    }

    def test_book_creation_incorrect_data(self):
        for incorect_input in self.incorrect_inputs:
            input = self.correct_inputs.copy()
            input.update({incorect_input: self.incorrect_inputs[incorect_input]})
            with self.assertRaises(ValueError):
                book = Book(**input)

    # testy wstrzyknięcia kodu SQL i JavaScript

    sql_injection = {
        "name": "Test Book'; DROP TABLE books; --",
        "author": "Test Author'; DROP TABLE books; --",
        "year_published": 2021,
        "book_type": "Fiction",
    }

    js_injection = {
        "name": "Test Book<script>alert('XSS')</script>",
        "author": "Test Author<script>alert('XSS')</script>",
        "year_published": 2021,
        "book_type": "Fiction",
    }

    def test_sql_injection(self):
        for incorect_input in self.sql_injection:
            input = self.correct_inputs.copy()
            input.update({incorect_input: self.sql_injection[incorect_input]})
            with self.assertRaises(ValueError):
                book = Book(**input)

    def test_js_injection(self):
        for incorect_input in self.js_injection:
            input = self.correct_inputs.copy()
            input.update({incorect_input: self.js_injection[incorect_input]})
            with self.assertRaises(ValueError):
                book = Book(**input)

    # testy ekstremalne
    def test_book_creation_empty(self):
        with self.assertRaises(ValueError):
            book = Book()

        with self.assertRaises(ValueError):
            empty_inputs = self.correct_inputs.copy()
            empty_inputs.update({"name": ""})
            book = Book(**empty_inputs)

    big_input = {
        "name": "X" * 10_000,
        "author": "X" * 10_000,
        "year_published": 1_000_000_000_000_000_000,
        "book_type": "X" * 10_000,
    }

    def test_big_data(self):
        for incorect_input in self.big_input:
            input = self.correct_inputs.copy()
            input.update({incorect_input: self.big_input[incorect_input]})
            with self.assertRaises(ValueError):
                book = Book(**input)


if __name__ == "__main__":
    unittest.main()
