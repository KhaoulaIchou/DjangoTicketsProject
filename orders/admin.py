from django.contrib import admin

# Register your models here.
from .models import Order  # Replace Event with your actual model name

admin.site.register(Order)  # Repeat this line for each model in the application

