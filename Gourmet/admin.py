from django.contrib import admin
from order_table.models import *

admin.site.register(Table)
admin.site.register(Ordered_Table)
admin.site.register(Client)
admin.site.register(DishToTable)