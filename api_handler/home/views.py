from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from django.shortcuts import render


def logout():
    pass

# TODO: Develop a home page with sidebar with options like all users count, viewing their products, etc.
class HomeView(LoginRequiredMixin, APIView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user = request.user
        context = {
            'email': user,
        }

        return render(request, 'home.html', context=context)
