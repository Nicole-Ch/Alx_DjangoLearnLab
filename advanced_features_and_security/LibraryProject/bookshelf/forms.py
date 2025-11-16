# bookshelf/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        """Secure title validation"""
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Title is required.")
        
        # Basic XSS prevention
        dangerous_patterns = ['<script>', '</script>', 'javascript:', 'onload=', 'onerror=']
        for pattern in dangerous_patterns:
            if pattern in title.lower():
                raise ValidationError("Invalid characters in title.")
        
        return title
    
    def clean_author(self):
        """Secure author validation"""
        author = self.cleaned_data.get('author', '').strip()
        if not author:
            raise ValidationError("Author is required.")
        
        # Allow only letters, spaces, hyphens, and apostrophes
        import re
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', author):
            raise ValidationError("Author name contains invalid characters.")
        
        return author
    
    def clean_publication_year(self):
        """Secure publication year validation"""
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 2030):
            raise ValidationError("Please enter a valid publication year (1000-2030).")
        return year