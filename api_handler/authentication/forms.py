from django import forms


class SignInForm(forms.Form):
    email = forms.CharField(label='Email',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password',
                               max_length=64,
                               widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Password'}))


class SignUpForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=64)
    confirm_password = forms.CharField(label='Password', max_length=64)
