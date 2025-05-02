from django.shortcuts import render
from django.http import JsonResponse
from order_table.models import *
from django.contrib.auth.decorators import login_required

# # Create your views here.
# @login_required(login_url='login')  # ЗРОБИТИ РЕГІСТРАЦІЮ І АВТОРИЗАЦІЮ
def order_table(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        table = Table.objects.get(id=table_id)
        order = Ordered_Table.objects.create(table=table)
        return JsonResponse({'order_id': order.id})
    tables = Table.objects.all()
    return render(request, 'order.html', {'tables': tables})