from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EmailOrUsernameTokenObtainPairView, RegisterUserView, UserApiViewSet, UserView

router = DefaultRouter()
router.register('users', UserApiViewSet, basename='users')

urlpatterns = [
    path('auth/me/', UserView.as_view(), name='auth-me'),
    path('auth/register/', RegisterUserView.as_view(), name='auth-register'),
    path('auth/token/', EmailOrUsernameTokenObtainPairView.as_view(), name='auth-token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('', include(router.urls)),
]
