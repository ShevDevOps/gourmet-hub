from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from order_table.models import *

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Перевірка, чи існує користувач із таким ім'ям або email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        # Створення нового користувача
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html')

def login_user(request):  # Змінили ім'я функції
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Використовуємо вбудовану функцію login
            return redirect('index')  # Перенаправлення на головну сторінку
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)  # Вихід користувача
    return redirect('index')