from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SignUpView,
    CustomTokenObtainPairView,
    UserMeAPIView,
    UserViewSet
)


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/users/me/', UserMeAPIView.as_view(), name='users-me'),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain'
    ),
]
