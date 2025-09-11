from django.urls import path
from .views import MyTokenObtainPairView, TokenRefreshView, register, logout, profile
from rest_framework_simplejwt.views import TokenRefreshView as SimpleTokenRefresh

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', SimpleTokenRefresh.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]

