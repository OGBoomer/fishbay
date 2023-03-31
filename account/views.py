from django.shortcuts import render, redirect
from .forms import CreateAccountForm
from django.contrib.auth import authenticate, login, logout


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('searchprofile:profile_list')

    return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'account/login.html')
        else:
            print("not valid")
    else:
        form = CreateAccountForm()
    return render(request, 'account/register.html', {'form':form})



