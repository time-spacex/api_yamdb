from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
]