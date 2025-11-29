from rest_framework import serializers
from .models import Book, Author
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    # Field-level validation for publication_year.
    # Raises ValidationError if the year is greater than the current year.
    def validate_publication_year(self, data):
            current_year = date.today().year
            if data > current_year:
                  raise serializers.ValidationError("Publication_year can't be in the future.")
            return data

# Minimal nested serializer for AuthorSerializer
class AuthorBookNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']

# Author serializer using the nested serializer
class AuthorSerializer(serializers.ModelSerializer):
    books = AuthorBookNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']    