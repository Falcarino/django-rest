from django.urls import path
from .views import UsersView
from ..products.views import UserProductsView

urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('<str:ids>', UsersView.as_view(), name='users'),
    path('<int:user_id>/products/', UserProductsView.as_view(), name='user_products')
]
