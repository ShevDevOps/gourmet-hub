from django.contrib import admin
from order_table.models import *
from dishes.models import *
from shefs.models import *

admin.site.register(Table)
admin.site.register(Ordered_Table)
admin.site.register(DishToTable)
admin.site.register(Dish)
admin.site.register(Ingredient)
admin.site.register(IngrToDish)
admin.site.register(Chef)
admin.site.register(ChefToDish)
admin.site.register(RecommendationTag)
admin.site.register(StandardCategory)