from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from .views import RegistrationAPI,SendVerficationAPI,ValidateVerificationView,UserAPI,UserLogout,UserDetailAPIView

urlpatterns = [
    path('register/', RegistrationAPI.as_view(), name = 'register_user'),
    path('logout/',  UserLogout.as_view(), name = 'logout_user'),
    path('login/', TokenObtainPairView.as_view(), name = 'login_user'),
    path('token-refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('email-verification/', SendVerficationAPI.as_view(), name = 'send-email-verification'),
    path('email-verification/<id>/<token>/', ValidateVerificationView.as_view(), name = 'verify-email'),
    path('user/', UserAPI.as_view(), name = 'user-data'),
    path('users/<str:username>/', UserDetailAPIView.as_view(), name='user-detail'),
]
