from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def dishes(request):
    dish = Dish.objects.all()
    return render(request, 'dishes.html', {'dishes': dish})