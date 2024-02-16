from django.contrib import admin
from .models import Profile, Contact, Booking, Trainer, SessionType
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Booking)
class BookinAdmin(SummernoteModelAdmin):
    list_display = ('user', 'trainer_name', 'session_type', 'date', 'time', 'name', 'phonenumber', 'email', 'age', 'gender', 'message', 'approved')
    search_fields = ('name', 'trainer_name', 'session_type', 'approved')  
    list_filter = ('trainer_name', 'session_type', 'date', 'approved')  
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name_contact', 'email', 'contact_message', 'created_on')
    list_filter = ('name_contact', 'email', 'created_on',)
    list_display_links = ('name_contact',)
    search_fields = ['name_contact', 'email', 'contact_message', 'created_on']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('user',)
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_number', 'email')  


admin.site.register(Trainer)
admin.site.register(SessionType)
# admin.site.register(Booking)