# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Account  
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, AccountUpdateForm
from django.contrib import messages
from .forms import UserRegisterForm, AccountRegisterForm  
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from events.models import Event
from orders.models import Order
from django.utils import timezone
from tickets.models import Ticket
from django.shortcuts import get_object_or_404, redirect


def dashboard_user(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        # Retrieve the event object
        event = Event.objects.get(pk=event_id)
        # Create the order
        order = Order.objects.create(user=request.user, event=event, total_amount=event.ticket_price, purchase_date=timezone.now())
        ticket = Ticket.objects.create(event=event, buyer=request.user, purchase_date=timezone.now())
        # Add tickets to the order (if applicable)
        # Replace the following line with your logic to add the appropriate tickets to the order
        #order.tickets.add(event)
        # Update the payment status (if applicable)
        order.payment_status = 'complete'
        # Save the order
        order.save()
        ticket.save()
        return redirect('dashboard_user')
    
    events = Event.objects.filter(status='approved')
    

   # Get the IDs of newly approved events from the user's session
    #new_event_ids = request.session.get('new_event_ids', [])

    # Filter events to include only the newly approved ones
    #new_events = events.filter(pk__in=new_event_ids)

    # Update the session with the IDs of newly approved events
    #new_event_ids = list(new_events.values_list('pk', flat=True))
    #request.session['new_event_ids'] = new_event_ids




    return render(request, 'accounts/dashboard_user.html', {'events': events})


def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    print(f"Orders: {orders}")  # Check the orders queryset in the console  
    context = {           
            'orders': orders
        }
    return render(request, 'accounts/user_orders.html', context)

def remove_ticket(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    event = order.event
    order.delete()
    # Redirect to the user's orders page
    return redirect('user_profile')

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        account_form = AccountRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserRegisterForm()
        account_form = AccountRegisterForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'account_form': account_form})

from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth.decorators import login_required


def admin(request):
    return render(request, 'accounts/admin.html')


def principal_page(request):
    return render(request, 'accounts/principal_page.html')


def user_check(user):
    return user.account.type_user == 'simple_user'

def organizer_check(user):
    return user.account.type_user == 'organizer'


@login_required(login_url='login')
def user_profile(request):
     account = Account.objects.get(user=request.user)
     orders = Order.objects.filter(user=request.user)
     print(f"Orders: {orders}")  # Check the orders queryset in the console
     context = {
        'account': account,
        'orders': orders
    }
     return render(request, 'accounts/user_profile.html', context)

@login_required(login_url='login')
def organizer_profile(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'accounts/organizer_profile.html', {'account': account})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user_check(user):
                return redirect('user_profile')
            elif organizer_check(user):
                return redirect('organizer_profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


from .models import Account  
from events.models import Event

def organizer_profile_view(request):
    if request.user.is_authenticated:
        print(f"Authenticated User: {request.user.username}")  # print username of authenticated user
        events = Event.objects.filter(organizer=request.user)
        print(f"Events: {events}")  # print queryset of events
        context = {
            'account': Account.objects.get(user=request.user),
            'events': events
        }
        return render(request, 'accounts/organizer_profile.html', context)
    else:
        print("User is not authenticated.")  # print a message if user is not authenticated
        return redirect('login')  # replace 'login' with the name of your login url



@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()

            # Update profile picture if a new one is provided
            if 'profile_pic' in request.FILES:
                account = request.user.account
                account.profile_pic = request.FILES['profile_pic']
                account.save()

            messages.success(request, 'Your account has been updated!')
            
            if organizer_check(request.user):
                return redirect('organizer_profile')
            else:
                return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        account_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'user_form': user_form,
        'account_form': account_form
    }

    return render(request, 'accounts/profile_update.html', context)


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Account

class AccountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Account
    fields = ['full_name', 'type_user', 'profile_pic', 'date_of_birth', 'phone_number', 'address', 'bio']

    def test_func(self):
        return self.request.user.is_superuser

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Account
    fields = ['full_name', 'type_user', 'profile_pic', 'date_of_birth', 'phone_number', 'address', 'bio']

    def test_func(self):
        return self.request.user.is_superuser

class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/'

    def test_func(self):
        return self.request.user.is_superuser

class AccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'accounts/account_list.html'
    ordering = ['-date_joined']

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(full_name__icontains=query)
        return qs

class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Account

    def test_func(self):
        return self.request.user.is_superuser