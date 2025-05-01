from django.shortcuts import render
from django.http import JsonResponse
from order_table.models import *

def register(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'User registered successfully!'})
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'User logged in successfully!'})
    return render(request, 'login.html')