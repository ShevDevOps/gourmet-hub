from django.shortcuts import render
from .models import Chef

# Create your views here.
def shefs(request):
    сhefs = Chef.objects.all()
    return render(request, 'shefs.html', {'chefs' : сhefs})

def shef_detail(request, shef_id):
    chef = Chef.objects.get(pk=shef_id)
    return render(request, 'shef_detail.html', {'chef': chef})