from django.contrib import admin

# Register your models here.
from .models import Ticket  # Replace Event with your actual model name

admin.site.register(Ticket)  # Repeat this line for each model in the application

