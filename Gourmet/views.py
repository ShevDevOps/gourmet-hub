from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from order_table.models import *

def register(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'User registered successfully!'})
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