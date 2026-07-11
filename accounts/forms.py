from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="نام کاربری")
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput,
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="ایمیل", required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )