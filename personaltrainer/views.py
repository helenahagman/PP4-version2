from django import forms
from django.urls import reverse
from django.core.mail import send_mail
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from .models import Profile, Contact, Booking, MemberComment
from .forms import (
    ContactForm,
    BookingForm,
    ProfileForm,
    SignUpForm,
    MemberCommentForm,
    LoginForm,
)

# renders the homepage
def index(request):
    """
    Renders the home view.
    """
    return render(request, 'index.html')

# view for the personal trainer page
class PersonalTrainerView(View):
    """
    Implementation for the PersonalTrainer view
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'personaltrainer.html')

# view for the members only page 
class MembersonlyView(View):
    """
    Implementation for the Membersonly view
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'membersonly.html')
        else:
            return redirect('login')

# view for booking a session
class BookView(LoginRequiredMixin, View):
    """
    Implementation for the book view
    """
    template_name = 'book.html'

    # @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        initial_data = {'email': request.user.email}
        form = BookingForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_instance = form.save(commit=False)
            booking_instance.user = request.user
            booking_instance.save()
            messages.success(request, 'Your session has been booked')
            return redirect('profile_view')

        return render(request, self.template_name, {'form': form})

# view for the member page
class MemberView(View):
    """
    Implementation for the Member view
    """
    template_name = 'member.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

# view for the profile page, shows profile info and booking requests
class ProfileView(LoginRequiredMixin, View):
    """
    Implementation for the User profile view
    """
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form = ProfileForm(instance=profile)
        bookings = Booking.objects.filter(user=user)

        context = {
            'form': form,
            'user': user,
            'profile': profile,
            'bookings': bookings,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile_view')
        bookings = Booking.objects.filter(user=user)
        return render(
            request,
            self.template_name,
            {
                'form': form,
                'user': user,
                'profile': profile,
                'bookings': bookings
            }
        )

# function for sign-up form
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('profile_view')
    else:
        form = SignupForm()

    return render(request, 'account/signup.html', {'form': form})

# login functionality
@csrf_protect
def log_in(request):
    """
    To log in the user and redirect to the profile page
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile_view')
    else:
        form = AuthenticationForm()

    context = {
        'title': 'Login',
        'form' : form,
    }
    return render(request, 'login.html', context)

# logout functionality
@login_required
def log_out(request):
    """
    To log out the user and redirect to start page
    """
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('index')

# renders the users profile page
@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    bookings = Booking.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        'bookings': bookings,
    }

    return render(request, 'profile.html', context)

# contact form submission and handling
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,
                             'Your message has been sent, '
                             'we will reply shortly.')
            return render(request, 'contact.html', {'form': ContactForm()})
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'email': request.user.email})
        else:
            form = ContactForm()

    return render(request, 'contact.html', {'form': form})

# cancellation funtionality for sessions, deletes the booking when cancelled
@login_required
def book_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.participant is None:
        session.participant = request.user
        session.save()
        messages.success(request, 'Your session is booked')
        return redirect('session_success_url')
    else:
        messages.error(request, 'This session is already booked')
        return render(request, 'session_already_booked.html')

# view for the personal trainer page
def personal_trainer(request):
    context = {
        'header': 'Personal Trainer',
        'subheading': (
            'A session with a Personal Trainer can make '
            'the whole difference.'
        ),
    }
    return render(request, 'personaltrainer.html', context)

# view for the member page
def members(request):
    context = {
        'header': 'Members',
        'subheading': (
            'As a member you get access to all the best '
            'offers and news!'
        ),
    }
    return render(request, 'member.html', context)

# view for the login page
def login(request):
    context = {
        'header': 'Stay active',
        'subheading': (
            'Daily exercise helps you to '
            'stay strong and healthy.'
        ),
    }
    return render(request, 'login.html', context)

# view for the signup page
def signup(request):
    context = {
        'header': 'Welcome',
        'subheading': (
            'Make smart choices and live a healthier life.'
        ),
    }
    return render(request, 'account/signup.html', context)

# view for the contact page
def contact(request):
    context = {
        'header': 'Contact us',
        'subheading': (
            'We are here for you, '
            'let us know whats on your mind'
        ),
    }
    return render(request, 'contact.html', context)

# view for the book session page
def book(request):
    context = {
        'header': 'Book PT session',
        'subheading': (
            'A session with an expert will get you started! '
        ),
    }
    return render(request, 'book.html', context)

# view for the members only page, including for submission for comments
@login_required
def membersonly(request):
    if request.method == 'POST':
        form = MemberCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('membersonly')
    else:
        form = MemberCommentForm()
    return render(request, 'membersonly.html', {'form': form})

# function to cancel a booking
@login_required
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(
            Booking, id=booking_id, user=request.user
            )
        
        booking.delete()
        messages.success(request,
                        "Your booking has been successfully canceled.")
    return redirect('profile_view')

# view for member comments
def share_journey(request):
    if request.method == 'POST':
        form = MemberCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('membersonly')
    else:
        form = MemberCommentForm()
    comments = MemberComment.objects.all().order_by('-created_at')
    return render(request, 'membersonly.html', {'form': form, 'comments': comments})
