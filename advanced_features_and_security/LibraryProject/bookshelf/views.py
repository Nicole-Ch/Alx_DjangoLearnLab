# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from .models import Book
from .forms import BookForm  # We'll create this

def book_list(request):
    """Safe book listing with search functionality"""
    books = Book.objects.all()
    query = request.GET.get('q', '').strip()
    
    # Safe search using Django ORM (prevents SQL injection)
    if query:
        # Use parameterized queries with Q objects
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    
    # Escape the query for safe display
    safe_query = escape(query)
    
    context = {
        'books': books,
        'query': safe_query,
    }
    return render(request, 'bookshelf/book_list.html', context)

@login_required
def form_example(request, book_id=None):
    """Secure form handling for adding/editing books"""
    book = None
    if book_id:
        book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Form data is validated and safe
            book = form.save()
            messages.success(request, f'Book "{escape(book.title)}" has been saved successfully.')
            return redirect('book_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'bookshelf/form_example.html', context)

@login_required
@require_http_methods(["POST"])  # Only allow POST requests
def delete_book(request, book_id):
    """Secure book deletion"""
    book = get_object_or_404(Book, id=book_id)
    book_title = escape(book.title)
    book.delete()
    messages.success(request, f'Book "{book_title}" has been deleted.')
    return redirect('book_list')

def safe_search(request):
    """Additional safe search view if needed"""
    query = request.GET.get('q', '').strip()
    results = Book.objects.none()
    
    if query:
        # Remove potentially dangerous characters
        import re
        safe_query = re.sub(r'[^\w\s\-]', '', query)
        results = Book.objects.filter(
            Q(title__icontains=safe_query) | Q(author__icontains=safe_query)
        )
    
    context = {
        'books': results,
        'query': escape(query),
    }
    return render(request, 'bookshelf/book_list.html', context)