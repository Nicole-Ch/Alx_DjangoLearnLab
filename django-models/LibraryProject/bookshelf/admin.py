from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for these fields in the right sidebar
    list_filter = ('publication_year', 'author')
    
    # Enable search for these fields
    search_fields = ('title', 'author')
    
    # Optional: Group fields in the detail view
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'author']
        }),
        ('Publication Details', {
            'fields': ['publication_year'],
            'classes': ['collapse']  # Makes this section collapsible
        }),
    ]