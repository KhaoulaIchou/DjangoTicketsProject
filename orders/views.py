from django.shortcuts import render
from .models import Order
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from events.models import Event
from tickets.models import Ticket

# Create your views here.


class EventDetailView(DetailView):
    model = Event

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []  # The fields will be automatically filled in form_valid method

    def form_valid(self, form):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        form.instance.user = self.request.user
        form.instance.event = ticket.event
        form.instance.total_amount = ticket.event.ticket_price
        form.instance.save()
        form.instance.tickets.add(ticket)
        ticket.buyer = self.request.user
        ticket.status = 'booked'
        ticket.save()
        ticket.event.tickets_available -= 1
        ticket.event.save()
        return super().form_valid(form)

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        for ticket in order.tickets.all():
            ticket.buyer = None
            ticket.status = 'available'
            ticket.save()
            ticket.event.tickets_available += 1
            ticket.event.save()
        return super().delete(request, *args, **kwargs)

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/user_orders.html'  
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
