from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from authentication.forms import SignInForm, SignUpForm
from users.models import User

class SignInView(APIView):

    def get(self, request):
        form = SignInForm()
        context = {
            'form': form,
        }

        return render(request, 'login.html', context=context)

    def post(self, request):
        signin_form = SignInForm(request.POST)

        if signin_form.is_valid():
            email = signin_form.cleaned_data['email']
            password = signin_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('Unauthorized', status=401)
        else:
            return HttpResponse('Unauthorized', status=401)


class SignUpView(APIView):

    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
            'passwords_match': True
        }
        return render(request, 'register.html', context=context)

    def post(self, request):
        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            confirm_password = signup_form.cleaned_data['confirm_password']

            passwords_match = password == confirm_password
            if passwords_match:
                new_user = User.objects.create_superuser(email=email, password=password)
                new_user.save()

                return redirect('login')
            else:
                # TODO: come up with a better way of rendering the message
                form = SignUpForm()
                context = {
                    'form': form,
                    'passwords_match': False
                }

                return render(request, 'register.html', context=context)
        else:
            return redirect('register')
