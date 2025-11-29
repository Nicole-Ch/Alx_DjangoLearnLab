from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # Create authors and books
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        self.book1 = Book.objects.create(title="Book One", publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2010, author=self.author2)

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        payload = {
            'title': 'Book Three',
            'publication_year': 2025,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.client.logout()

    def test_create_book_unauthenticated(self):
        payload = {
            'title': 'Book Three',
            'publication_year': 2025,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # because permissions are IsAuthenticatedOrReadOnly

    def test_filter_books_by_author(self):
        response = self.client.get('/api/books/?author__name=Author One')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book One")

    def test_search_books(self):
        response = self.client.get('/api/books/?search=Two')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book Two")

    def test_ordering_books(self):
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.data[0]['title'], "Book Two")
        self.assertEqual(response.data[1]['title'], "Book One")

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        payload = {'title': 'Updated Book One'}
        response = self.client.patch(f'/api/books/{self.book1.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book One')
        self.client.logout()

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
        self.client.logout()
