from django.urls import include, path

urlpatterns = [
    path('users/', include('api_handler.users.urls')),
    path('products/', include('api_handler.products.urls'))
]
