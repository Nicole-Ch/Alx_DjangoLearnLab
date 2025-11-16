from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('relationship_app.can_add_book')
def add_book(request):
    return render(request, 'add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    return render(request, 'edit_book.html')

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    return render(request, 'delete_book.html')