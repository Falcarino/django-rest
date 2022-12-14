from django.urls import path

from products.views import UserProductsView
from .views import UsersView

urlpatterns = [
    path('', UsersView.as_view(), name='all_users'),
    path('<str:ids>', UsersView.as_view(), name='users'),
    path('<int:user_id>/products/', UserProductsView.as_view(), name='user_products')
]
