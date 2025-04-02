from django.urls import path
from accounts.views import SignupView, LoginView

urlpatterns = [
    path('api/v1/signup/', SignupView.as_view(), name='signup'),
    path('api/v1/login/', LoginView.as_view(), name='login'),
]
