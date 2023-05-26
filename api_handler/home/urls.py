from django.urls import path
from .views import HomeView
from users.views import UsersWebView
from products.views import ProductsWebView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('users', UsersWebView.as_view(), name='users_web'),
    path('products', ProductsWebView.as_view(), name='products_web')
]
