from django.urls import path, include

urlpatterns = [
    path('users/', include('api_handler.users.urls'))
]