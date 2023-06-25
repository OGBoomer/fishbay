from django.shortcuts import render, redirect
from .admin import UserCreationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth import get_user_model


# User = get_user_model()


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('account:homepage')
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print('in login')
        if user is not None:
            print('user not none')
            login(request, user)
            return redirect('account:homepage')
        else:
            messages.error(request, 'Login Failed')
    return render(request, 'account/login.htmx')


def register(request):
    if request.user.is_authenticated:
        return redirect('account:homepage')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("before valid")
        if form.is_valid():
            print('before save')
            form.save()
            return render(request, 'account/login.htmx')
        else:
            print("not valid")
    else:
        form = UserCreationForm()
    return render(request, 'account/register.htmx', {'form': form})


def logoutpage(request):
    print('before')
    logout(request)
    print("after")
    return redirect('account:loginpage')


def homepage(request):
    return render(request, 'account/home.html')
