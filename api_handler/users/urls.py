from django.urls import path
from .views import UsersView

urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('<str:ids>', UsersView.as_view(), name='users')
]