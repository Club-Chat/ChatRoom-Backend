from django.urls import path
from .views import ForgotPasswordView, RegisterView, LoginView, LogoutView, ProfileView, ResetPasswordView, UpdatePasswordView, UpdateProfileView, UserListView, csrf

urlpatterns = [
    path('csrf/', csrf, name='csrf'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('update-password/', UpdatePasswordView.as_view()),
    path('update-profile/', UpdateProfileView.as_view()),
    path('users/', UserListView.as_view()),
]