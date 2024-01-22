from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    USER_TYPES = (
        ('organizer', 'Organizer'),
        ('simple_user', 'Simple User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    type_user = models.CharField(max_length=12, choices=USER_TYPES, default='simple_user')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        print("Saving Account model")
        super().save(*args, **kwargs)

