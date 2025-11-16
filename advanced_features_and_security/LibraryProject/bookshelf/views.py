# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .forms import ExampleForm, BookForm
from .models import Book

def example_form_view(request):
    """
    View demonstrating secure form handling with ExampleForm
    Includes CSRF protection, validation, and secure data processing
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Form data is validated and safe to use
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Process the secure data here (e.g., save to database, send email)
            messages.success(
                request, 
                f"Thank you, {name}! Your message has been received securely."
            )
            return redirect('book_list')
        else:
            messages.error(
                request,
                "Please correct the errors below. Potential security issues were detected."
            )
    else:
        form = ExampleForm()
    
    context = {
        'form': form,
        'title': 'Secure Example Form'
    }
    return render(request, 'bookshelf/form_example.html', context)

# ADD THESE NEW PERMISSION-PROTECTED VIEWS - DON'T CHANGE EXISTING ONES

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View that requires can_view permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View that requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required  
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    """View that requires can_edit permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    """View that requires can_delete permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully.')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})