from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from personaltrainer.utils import num_validation, alpha_only

# model to store booking information for personal trainer sessions
class Booking(models.Model):
    """
    Create a booking request form for a personal trainer session
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    trainer_name = models.ForeignKey('Trainer', on_delete=models.CASCADE)
    session_type = models.ForeignKey('SessionType', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=100, default='Your name')
    phonenumber = models.CharField(max_length=15, default='1234567890')
    email = models.EmailField(max_length=70, default='your@mail.com')
    age = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    gender = models.CharField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        default='male'
    )
    message = models.TextField(max_length=300, default='', blank=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='pending')

    def __str__(self):
        return (
            f'Booking by {self.user.username} for {self.session_type} '
            f'session with {self.trainer_name} on {self.date} at {self.time}'
        )

    def get_approval_status_display(self):
        return dict(Booking.STATUS_CHOICES)[self.status]

# model to represent personal trainers
class Trainer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# model to represent personal trainer session choices
class SessionType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

# model for storing contact messages from users
class Contact(models.Model):
    """
    Model for contact messages.
    """
    name_contact = models.CharField(max_length=100)
    email = models.EmailField(max_length=70, default='default@example.com')
    contact_message = models.TextField(max_length=400, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return (
            f'Contact message submitted by {self.name_contact}'
            f'on {self.created_on}'
        )

# model to represent user profiles
class Profile(models.Model):
    """
    User profile
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
        )
    email = models.EmailField(max_length=70, default='default@example.com')
    phone_number = models.CharField(max_length=20, null=True, blank=True,
                                    validators=[num_validation])
    first_name = models.CharField(max_length=50, null=True, blank=True,
                                  validators=[alpha_only])
    last_name = models.CharField(max_length=50, null=True, blank=True,
                                 validators=[alpha_only])

    def __str__(self):
        return f'{self.user} profile'

# model for member comments
class MemberComment(models.Model):
    """
    Member comments
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    photo = models.ImageField(upload_to='member_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
