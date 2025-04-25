from django.shortcuts import render
from django.http import JsonResponse
from order_table.models import *

# Create your views here.
def order_table(request):
    tables = Table.objects.all()
    return render(request, 'order_table.html', {'tables': tables})