from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm

# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "users/register.html", {"form":form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            return render(request, "users/register.html", {"form":form})

class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")