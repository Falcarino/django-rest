from django.urls import path, include

urlpatterns = [
    path('users/', include('api_handler.users.urls')),
    path('products/', include('api_handler.products.urls'))
]
