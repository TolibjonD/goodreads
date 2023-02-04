from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from users.models import CustomUser
from django.core.paginator import Paginator

# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "users/register.html", {"form":form})

    def post(self, request):
        form = RegisterForm(data=request.POST , files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered.")
            return redirect('users:login')
        else:
            return render(request, "users/register.html", {"form":form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form":form})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('landing_page')
        else:
            return render(request, "users/login.html", {"form":form})

class ProfilePageView(LoginRequiredMixin , View):
    def get(self, request):
        user = get_user(self.request)
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', {'user':request.user, "form":form})
    def post(self, request):
        user = get_user(self.request)
        form = UserUpdateForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully update your profile !...")
            return redirect('users:profile')
        else:
            return render(request, "users/update.html", {"form":form})

class LogoutView( LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully logged out.')
        return redirect('landing_page')

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_user(self.request)
        form = UserUpdateForm(instance=user)
        return render(request, "users/update.html", {"form":form})
    def post(self, request):
        user = get_user(self.request)
        form = UserUpdateForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully update your profile !...")
            return redirect('users:profile')
        else:
            return render(request, "users/update.html", {"form":form})

class UsersView(LoginRequiredMixin,UserPassesTestMixin, View):
    def get(self, request):
        users = CustomUser.objects.all().order_by('-id')
        search = request.GET.get('q', '')
        if search:
            users = CustomUser.objects.filter(first_name__icontains=search)
        paginator = Paginator(users, 5)
        page = request.GET.get('page', 1)
        pages = paginator.get_page(page)
        return render(request, "users/users.html", {"pages":pages, "search":search})
    def test_func(self):
        return self.request.user.is_superuser