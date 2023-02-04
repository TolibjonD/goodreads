from django.urls import path
from .views import RegisterView, LoginView, ProfilePageView, LogoutView, ProfileUpdateView, UsersView


app_name = "users"
urlpatterns = [
    path('register/' , RegisterView.as_view() , name="register"),
    path('login/' , LoginView.as_view() , name='login'),
    path('logout/' , LogoutView.as_view() , name='logout'),
    path( 'profile/update/', ProfileUpdateView.as_view() , name='update' ),
    path('users/' , UsersView.as_view() , name='users'), 
    path('profile/' , ProfilePageView.as_view() , name='profile')
]
