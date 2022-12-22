from django import forms


class SignInForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=64)


class SignUpForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=64)
    confirm_password = forms.CharField(label='Password', max_length=64)
