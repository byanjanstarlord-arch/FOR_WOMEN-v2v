from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            error = "Invalid email or password."
    return render(request, 'auth/login.html', {'error': error})

def signup_view(request):
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=email).exists():
            error = "An account with this email already exists."
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            login(request, user)
            return redirect('accounts:onboarding')
            
    return render(request, 'auth/signup.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('core:landing')

@login_required
def onboarding_view(request):
    if request.method == 'POST':
        user = request.user
        user.dream_career = request.POST.get('dream_career', '')
        user.save()
        return redirect('dashboard:index')
    return render(request, 'auth/onboarding.html')
