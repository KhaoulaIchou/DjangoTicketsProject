from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Event
from django.views.generic import ListView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



# Create your views here.

class EventDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = 'events/dashboard.html'
    context_object_name = 'events'

    def test_func(self):
        return self.request.user.is_superuser


from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from .models import Event

def organizer_check(user):
    return user.is_authenticated and user.account.type_user == 'organizer'

from django.views.generic.edit import FormMixin
from .forms import EventForm


from django.views.generic.edit import FormMixin
from .forms import EventForm

from django.http import JsonResponse

from django.http import JsonResponse

class OrganizerEventListView(FormMixin, ListView):
    model = Event
    template_name = 'events/organizer_event_list.html'
    form_class = EventForm
    success_url = '/events/organizer/events/'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        event = form.save(commit=False)

        # Handle the image file separately
        image_file = self.request.FILES.get('image')
        if image_file:
            file_name = default_storage.save('event_images/' + image_file.name, ContentFile(image_file.read()))
            event.image = file_name

        event.save()

        if self.request.is_ajax():
            data = {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'location': event.location,
                'date_time': str(event.date_time),
                'ticket_price': str(event.ticket_price),
                'tickets_available': event.tickets_available,
            }
            return JsonResponse(data)
        else:
            return super().form_valid(form)

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.get_queryset()
        return context
class EventCreateView(UserPassesTestMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'location', 'date_time', 'ticket_price', 'image', 'tickets_available']
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return organizer_check(self.request.user)



from django.http import JsonResponse

from django.http import JsonResponse

from django.views.generic.edit import UpdateView
from django.http import JsonResponse

class EventUpdateView(UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'location', 'date_time', 'ticket_price', 'image', 'tickets_available']
    success_url = reverse_lazy('organizer_event_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        response = super().form_valid(form)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            data = {
                'title': self.object.title,
                'description': self.object.description,
                'location': self.object.location,
                'date_time': str(self.object.date_time),
                'ticket_price': str(self.object.ticket_price),
                'tickets_available': self.object.tickets_available,
            }
            return JsonResponse(data)
        else:
            return response

    def put(self, request, *args, **kwargs):
        # Handle PUT requests here
        return self.post(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Handle PATCH requests here
        return self.post(request, *args, **kwargs)




class EventDeleteView(UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('organizer_event_list')
    login_url = 'login'
    raise_exception = True

    def test_func(self):
        return organizer_check(self.request.user)

from django.views.generic import ListView
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'events'
    ordering = ['date_time']
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Event.objects.filter(
                Q(location__icontains=query) & 
                Q(status='approved')
            )
        else:
            return Event.objects.filter(status='approved')


from django.shortcuts import render, get_object_or_404
from .models import Event



def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'accounts/event_detail.html', {'event': event})


class UserEventListView(ListView):
    model = Event
    template_name = 'events/user_events.html' 
    context_object_name = 'events'
    ordering = ['-date_time'] 
    paginate_by = 5