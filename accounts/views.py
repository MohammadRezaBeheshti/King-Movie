from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return "/"
    
class UserLogoutView(LogoutView):
    next_page = "/"