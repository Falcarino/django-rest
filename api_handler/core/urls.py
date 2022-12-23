from django.urls import include, path
from django.contrib import admin
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('', lambda request: redirect('home/', permanent=False)),
    path('auth/', include('authentication.urls')),
    path('home/', include('home.urls'))
]
