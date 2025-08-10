from django.urls import path
from .views import UserProfileView, PasswordResetView

urlpatterns = [
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('auth/password-reset/', PasswordResetView.as_view(), name='password-reset'),
]