from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
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