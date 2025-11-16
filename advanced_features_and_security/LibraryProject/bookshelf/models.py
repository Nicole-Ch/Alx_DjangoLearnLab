from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None, **extra_fields):
        """
        Create and return a regular user with an email and date of birth.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None, **extra_fields):
        """
        Create and return a superuser with an email and date of birth.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, date_of_birth, password, **extra_fields)

class CustomUser(AbstractUser):
    # Remove username and use email as the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

# Your existing Book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title
    
class Meta:
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]   
