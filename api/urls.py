from django.urls import path

from .views import (CustomUserLoginView, CustomUserRegistrationView,
                    GlobalDbView, SpamView)

urlpatterns = [
    path('v1/registeration', CustomUserRegistrationView.as_view(), name='register'),
    path('v1/login', CustomUserLoginView.as_view(), name='login'),
    path('v1/spam', SpamView.as_view(), name='spam'),
    path('v1/globaldb', GlobalDbView.as_view(), name='global'),
]
