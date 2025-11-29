from rest_framework import serializers
from .models import Book, Author
from datetime import date


class BookSerializer(serializers.ModelSerializer):
       class Meta:
            model = Book
            fields = "__all__"

    # Field-level validation for publication_year.
    #Raises ValidationError if the year is greater than the current year.
       def validate_publication_year(self, data):
            current_year = date.today().year
            if data > current_year:
                  raise serializers.ValidationError("Publication_year can't be in the future.")
            return data

class AuthorSerializer(serializers.ModelSerializer):

    """ Serializes Author with a nested list of books.
    - name: author's name
    - books: nested Book representations using AuthorBookNestedSerializer.
    This uses the related_name 'books' defined on Book.author. """
    
    books = BookSerializer(many=True)

    class Meta:
            model = Author     
            fields = ['name', 'books']       