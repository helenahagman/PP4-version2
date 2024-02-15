from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personal-trainer/', views.PersonalTrainerView.as_view(), name='personal_trainer'),
    path('members-only/', views.membersonlyView.as_view(), name='members_only'),
    path('member/', views.MemberView.as_view(), name='member'),
    path('book/', views.BookView.as_view(), name='book_session'),
    path('profile/', views.ProfileView.as_view(), name='profile_view'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('contact/', views.contact_view, name='contact'),
]