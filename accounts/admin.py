import profile
from django.contrib import admin
# Register your models here.
from .models import Account  # Replace Event with your actual model name

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'type_user', 'phone_number', 'address']
    list_filter = ['type_user']
    search_fields = ['user__username', 'full_name', 'phone_number']

admin.site.register(Account, AccountAdmin)



