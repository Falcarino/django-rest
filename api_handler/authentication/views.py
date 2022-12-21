from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse


class SignInForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=64)


class SignInView(APIView):

    def get(self, request):
        form = SignInForm()
        context = {
            'form': form,
        }
        return render(request, 'login.html', context=context)

    def post(self, request):
        form = SignInForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('Unauthorized', status=401)
        else:
            return HttpResponse('Unauthorized', status=401)


# TODO: Registering a new user
class SignUpView(APIView):

    def get(self, request):
        pass
