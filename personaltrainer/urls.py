from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from .views import (
    PersonalTrainerView,
    MembersonlyView,
    BookView,
    MemberView,
    ProfileView,
    
)


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('personal-trainer/', views.PersonalTrainerView.as_view(), name='personal_trainer'),
    path('members-only/', views.MembersonlyView.as_view(), name='members_only'),
    path('member/', views.MemberView.as_view(), name='member'),
    path('book/', views.BookView.as_view(), name='book_session'),
    path('profile/', views.ProfileView.as_view(), name='profile_view'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.log_in, name='login'),
    path('accounts/logout/', views.log_out, name='logout'),
    path('contact/', views.contact_view, name='contact'),
]