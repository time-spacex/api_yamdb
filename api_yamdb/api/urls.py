from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import SignUpView, CustomTokenObtainPairView, UserMeUpdateAPIView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/users/me/', UserMeUpdateAPIView.as_view(), name='user-me-update'),
]