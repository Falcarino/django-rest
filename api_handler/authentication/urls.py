from django.urls import path
from .views import SignInView
from .views import SignUpView

urlpatterns = [
    path('', SignInView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register')
]
