# bookshelf/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re

class ExampleForm(forms.Form):
    """
    ExampleForm for demonstrating secure form handling with CSRF protection,
    input validation, and XSS prevention as required by security best practices.
    """
    
    # Form fields with proper validation
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Your Name',
        help_text='Enter your full name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    
    email = forms.EmailField(
        max_length=150,
        required=True,
        label='Email Address',
        help_text='Enter a valid email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'your@email.com'
        })
    )
    
    message = forms.CharField(
        required=True,
        label='Message',
        help_text='Enter your message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your message here...',
            'rows': 4
        })
    )
    
    age = forms.IntegerField(
        required=False,
        label='Age',
        min_value=0,
        max_value=120,
        help_text='Optional: Enter your age',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Age'
        })
    )
    
    agree_to_terms = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
        help_text='You must agree to proceed'
    )

    def clean_name(self):
        """Secure name validation with XSS prevention"""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError("Name is required.")
        
        # XSS prevention - check for dangerous patterns
        dangerous_patterns = ['<script>', '</script>', 'javascript:', 'onload=', 'onerror=']
        for pattern in dangerous_patterns:
            if pattern in name.lower():
                raise ValidationError("Invalid characters in name.")
        
        # Allow only letters, spaces, hyphens, and apostrophes
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', name):
            raise ValidationError("Name contains invalid characters. Only letters, spaces, hyphens, and apostrophes are allowed.")
        
        return name

    def clean_message(self):
        """Secure message validation"""
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise ValidationError("Message is required.")
        
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        
        # Basic XSS prevention
        if '<script>' in message.lower():
            raise ValidationError("Message contains invalid content.")
        
        return message

    def clean(self):
        """Form-wide validation"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        agree_to_terms = cleaned_data.get('agree_to_terms')
        
        # Example of cross-field validation
        if email and 'test' in email.lower() and not agree_to_terms:
            raise ValidationError("Test emails must agree to terms.")
        
        return cleaned_data

# Keep your existing BookForm if you have it
class BookForm(forms.ModelForm):
    pass