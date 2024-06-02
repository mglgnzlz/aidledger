from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("NGO/GOVT", "NGO/GOVT"),
        ("HANDLER", "HANDLER"),
        ("RECIPIENT", "RECIPIENT"),
    )
    
    userType = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='RECIPIENT')
    accountName = models.CharField(max_length=25, null=True, default='Default Account Name')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change the related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change the related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )