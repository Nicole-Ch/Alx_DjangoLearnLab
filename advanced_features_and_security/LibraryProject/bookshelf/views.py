# bookshelf/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ExampleForm, BookForm

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