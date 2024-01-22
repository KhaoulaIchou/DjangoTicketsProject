from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from tickets.models import Ticket

# Create your models here.
class Order(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('complete', 'Complete'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateTimeField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')

    def __str__(self):
        return f"Order {self.pk}"