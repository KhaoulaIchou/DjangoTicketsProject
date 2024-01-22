from django.shortcuts import render
from .models import Ticket
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Ticket
from events.models import Event

# Create your views here.
class OrganizerTicketListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ticket
    template_name = 'tickets/organizer_tickets.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tickets'
    paginate_by = 10

    def test_func(self):
        return self.request.user.account.type_user == 'organizer'

    def get_queryset(self):
        organizer = self.request.user
        return Ticket.objects.filter(event__organizer=organizer)


class TicketCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ticket
    fields = ['event', 'ticket_type', 'status', 'tickets_available']

    def test_func(self):
        return self.request.user.account.type_user == 'organizer'

    def form_valid(self, form):
        form.instance.event.organizer = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['event', 'ticket_type', 'status', 'tickets_available']

    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.event.organizer


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'

    def test_func(self):
        ticket = self.get_object()
        return self.request.user == ticket.event.organizer


