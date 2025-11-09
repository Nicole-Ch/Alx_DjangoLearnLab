# relationship_app/query_samples.py
"""
Sample queries for the relationship_app.

Usage:
  # From the project root (where manage.py lives)
  python relationship_app/query_samples.py

  # Or from the manage.py shell:
  python manage.py shell
  >>> from relationship_app import query_samples
  >>> query_samples.books_by_author('Jane Doe')
"""

import os
import django
from typing import Iterable

# Ensure this points to your settings module. Change if your package name differs.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian  # noqa: E402


def books_by_author(author_name: str) -> Iterable[Book]:
    """
    Query all books by a specific author (by exact name).
    Returns a QuerySet of Book objects.
    """
    return Book.objects.filter(author__name=author_name)


def books_by_author_id(author_id: int) -> Iterable[Book]:
    """
    Query all books by a specific author (by author PK).
    """
    return Book.objects.filter(author_id=author_id)


def books_in_library(library_name: str) -> Iterable[Book]:
    """
    List all books in a library (by library name).
    Returns a QuerySet of Book objects.
    """
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Book.objects.none()
    return lib.books.all()


def librarian_for_library(library_name: str) -> Librarian | None:
    """
    Retrieve the Librarian for a library (OneToOne relation).
    Returns a Librarian instance or None if not found.
    """
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None

    # since library.librarian uses related_name='librarian' in models,
    # accessing lib.librarian will raise Librarian.DoesNotExist if none exists.
    try:
        return lib.librarian
    except Librarian.DoesNotExist:
        return None


# Small helper to pretty-print query results
def _print_qs(qs):
    for item in qs:
        print(f"- {item} (id={getattr(item, 'id', 'n/a')})")


if __name__ == "__main__":
    # Demo run: create tiny sample data if none exists, then run the three queries.
    if not Author.objects.exists():
        print("No data found — creating sample data...")
        a = Author.objects.create(name="Jane Doe")
        b1 = Book.objects.create(title="Django Tips", author=a)
        b2 = Book.objects.create(title="Advanced ORM", author=a)
        lib = Library.objects.create(name="Central Library")
        lib.books.add(b1, b2)
        Librarian.objects.create(name="Sam", library=lib)
        print("Sample data created.\n")

    # 1) Query all books by a specific author
    print("Books by author 'Jane Doe':")
    _print_qs(books_by_author("Jane Doe"))
    print()

    # 2) List all books in a library
    print("Books in library 'Central Library':")
    _print_qs(books_in_library("Central Library"))
    print()

    # 3) Retrieve the librarian for a library
    lib_name = "Central Library"
    lib_librarian = librarian_for_library(lib_name)
    if lib_librarian:
        print(f"Librarian for '{lib_name}': {lib_librarian.name} (id={lib_librarian.id})")
    else:
        print(f"No librarian found for '{lib_name}'.")
