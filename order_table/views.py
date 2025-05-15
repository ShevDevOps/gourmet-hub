from django.shortcuts import render
from django.http import JsonResponse
from order_table.models import *
from django.contrib.auth.decorators import login_required

# # Create your views here.
@login_required(login_url='login')
def order_table(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        client_num = request.POST.get('people_count')
        date_ = request.POST.get('date')  # Отримуємо дату з форми

        # Отримуємо столик
        table = Table.objects.get(id=table_id)

        # Перевірка місткості столика
        if int(client_num) > table.capacity:
            return JsonResponse({'error': 'Number of people exceeds table capacity.'}, status=400)

        # Створення замовлення
        order = Ordered_Table.objects.create(
            Client_Id=request.user,
            Client_num=client_num,
            Order_time=date_,
            capacity=table.capacity,
        )

        return render(request, 'index.html', {'order': order})
    tables = Table.objects.all()
    return render(request, 'order.html', {'tables': tables})