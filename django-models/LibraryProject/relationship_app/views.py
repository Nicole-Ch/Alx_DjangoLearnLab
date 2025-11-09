from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book, Librarian, UserProfile, Library, Author
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import BookForm

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the user in after signup
            return redirect('profile')  # redirect to profile page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def is_admin(user):
    """Check if user has Admin role"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        # Create UserProfile if it doesn't exist
        UserProfile.objects.create(user=user, role='Member')
        return False

def is_librarian(user):
    """Check if user has Librarian role"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user, role='Member')
        return False

def is_member(user):
    """Check if user has Member role"""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user, role='Member')
        return False

# ------------------------
# Role-based views
# ------------------------
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    """Admin dashboard - only accessible to users with Admin role"""
    context = {
        'user': request.user,
        'role': request.user.userprofile.role,
        'total_users': User.objects.count(),
        'total_books': Book.objects.count(),
        'total_libraries': Library.objects.count(),
    }
    return render(request, 'relationship_app/admin_view.html', context)

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian dashboard - only accessible to users with Librarian role"""
    # Get libraries managed by this librarian
    try:
        librarian = Librarian.objects.get(name=request.user.username)
        library = librarian.library
        books_in_library = library.books.all()
    except Librarian.DoesNotExist:
        library = None
        books_in_library = Book.objects.none()
    
    context = {
        'user': request.user,
        'role': request.user.userprofile.role,
        'library': library,
        'books_count': books_in_library.count() if library else 0,
        'recent_books': books_in_library.order_by('-id')[:5] if library else [],
    }
    return render(request, 'relationship_app/librarian_view.html', context)

@login_required
@user_passes_test(is_member)
def member_view(request):
    """Member dashboard - only accessible to users with Member role"""
    all_books = Book.objects.all()
    libraries = Library.objects.all()
    
    context = {
        'user': request.user,
        'role': request.user.userprofile.role,
        'total_books_available': all_books.count(),
        'libraries': libraries,
        'recent_books': all_books.order_by('-id')[:10],
    }
    return render(request, 'relationship_app/member_view.html', context)

# ------------------------
# Book management views with permission_required decorator
# ------------------------
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, 'relationship_app/book_form.html', context)

@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """View to edit a book - requires can_change_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'action': 'Edit',
        'book': book
    }
    return render(request, 'relationship_app/book_form.html', context)

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """View to delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    context = {
        'book': book
    }
    return render(request, 'relationship_app/confirm_delete.html', context)