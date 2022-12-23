from django.urls import path
from .views import SignInView, SignUpView, LogoutView

urlpatterns = [
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignUpView.as_view(), name='register')
]
