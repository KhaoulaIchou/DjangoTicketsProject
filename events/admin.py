from django.contrib import admin

# Register your models here.

from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'start_date', 'end_date', 'location', 'status']
    list_filter = ['status', 'start_date']
    search_fields = ['title', 'organizer__account__full_name', 'location']


    actions = ['approve_events', 'reject_events']  # Define custom admin actions

    def approve_events(self, request, queryset):
        queryset.update(status='approved')
    approve_events.short_description = 'Approve selected events'

    def reject_events(self, request, queryset):
        queryset.update(status='rejected')
    reject_events.short_description = 'Reject selected events'


admin.site.register(Event, EventAdmin)


