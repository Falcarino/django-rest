from django.urls import path

from .views import ProductsView

urlpatterns = [
    path('', ProductsView.as_view(), name='all_products'),
    path('<str:ids>', ProductsView.as_view(), name='products')
]
