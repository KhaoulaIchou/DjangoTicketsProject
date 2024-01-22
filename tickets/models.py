from django.db import models
from django.contrib.auth.models import User
from events.models import Event

# Create your models here.
class Ticket(models.Model):
    TICKET_STATUS = (
        ('available', 'Available'),
        ('booked', 'Booked'),
    )

    TICKET_TYPES = (
        ('regular', 'Regular'),
        ('vip', 'VIP'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_date = models.DateTimeField(blank=True, null=True)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES, default='regular')
    status = models.CharField(max_length=10, choices=TICKET_STATUS, default='available')
