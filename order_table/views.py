from django.shortcuts import render
from django.http import JsonResponse
from order_table.models import *
from django.contrib.auth.decorators import login_required

# # Create your views here.
# @login_required(login_url='login')  # ЗРОБИТИ РЕГІСТРАЦІЮ І АВТОРИЗАЦІЮ
def order_table(request):
    tables = Table.objects.all()
    return render(request, 'order.html', {'tables': tables})