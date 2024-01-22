from django.urls import path
from . import views
from .views import (OrganizerTicketListView, 
                    TicketCreateView, 
                    TicketUpdateView, 
                    TicketDeleteView)

urlpatterns = [
    #path('tickets/', views.tickets, name='tickets'),
    #path('tickets/<int:ticket_id>/book/', views.book_ticket, name='book_ticket'),
    #path('tickets/<int:ticket_id>/cancel/', views.cancel_ticket, name='cancel_ticket'),
    path('organizer/tickets/', OrganizerTicketListView.as_view(), name='organizer-tickets'),
    path('ticket/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]
