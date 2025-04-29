from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dishes(request):
    return render(request, 'dishes.html')