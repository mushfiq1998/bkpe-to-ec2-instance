from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, )

from .views import RegisterView, LogoutAPIView, SetNewPasswordAPIView, VerifyEmail, LoginAPIView, \
    PasswordTokenCheckAPI, RequestPasswordResetEmail, ResendVerifyEmail, FileUploadView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    # path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('resend-email-verify/', ResendVerifyEmail.as_view(), name="resend-email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('importUser', FileUploadView.as_view(), name="user-import")
]
