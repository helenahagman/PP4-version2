import datetime
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ValidationError
from .models import Contact, Booking, Profile, MemberComment
from django.utils import timezone
from datetime import date

# get the custom user model
User = get_user_model()


# form for submitting the contact message
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name_contact', 'email', 'contact_message']
        widgets = {
            'name_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'contact_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }

# function for time choices for booking time
def time_choices():
    start = datetime.time(8, 0)
    end = datetime.time(22, 0)
    interval = datetime.timedelta(minutes=30)

    times = []
    current = start
    while current <= end:
        times.append(current.strftime('%H:%M'))
        current = (datetime.datetime.combine(datetime.date.today(),
                   current) + interval).time()

    return [(time, time) for time in times]

# form for making a booking
class BookingForm(forms.ModelForm):
    time = forms.ChoiceField(choices=time_choices(), widget=forms.Select)

    class Meta:
        model = Booking
        fields = ['trainer_name', 'session_type', 'date', 'time', 'name',
                  'phonenumber', 'email', 'age', 'gender', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'trainer_name': forms.Select(),
            'session_type': forms.Select(),
            'date': forms.DateInput(attrs={
                'type': 'date', 'min': timezone.now().date().isoformat()}),
        }

    def clean_age(self):
        input_age = self.cleaned_data['age']
        if input_age < 18:
            raise ValidationError("You must be at least 18 years old to book.")
        return input_age

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

# form for editing the user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']

# form for user sign in
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required information')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

# form for user login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

# form for submitting member comments
class MemberCommentForm(forms.ModelForm):
    class Meta:
        model = MemberComment
        fields = ['comment', 'photo']
