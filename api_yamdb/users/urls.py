from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, CustomTokenObtainPairView, UserMeAPIView, UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('v1/users/me/', UserMeAPIView.as_view(), name='users-me'),
]