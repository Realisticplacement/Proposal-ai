from django.urls import path
from .views import LoginViewSet, MeView, RegisterViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
    path('refresh/', LoginViewSet.as_view({'post': 'refresh'}), name='token-refresh'),
    path('me/', MeView.as_view(), name='me'),
]