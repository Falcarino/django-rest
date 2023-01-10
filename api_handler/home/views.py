from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from django.shortcuts import render


class HomeView(LoginRequiredMixin, APIView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user
        context = {
            'email': user,
        }

        return render(request, 'home.html', context=context)
