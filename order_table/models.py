from django.db import models
from django.core.exceptions import ValidationError
from dishes.models import Dish
from django.contrib.auth.models import User

class Table(models.Model):
    capacity = models.IntegerField()

    def __str__(self):
        a = f"Table {self.id} (Capacity: {self.capacity})"
        if self.is_available: a += " - Available"
        else: a += " - Not Available"
        return a

class Ordered_Table(Table):
    Client_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    Client_num = models.IntegerField()
    Order_time = models.DateField()

    def clean(self):
        if self.capacity < self.Client_num:
            raise ValidationError("Client number exceeds table capacity.")
        super().clean()

    def __str__(self):
        a = f"Order {self.id} for {self.Client_Id} on {self.Order_time}"
        return a
    
class DishToTable(models.Model):
    table = models.ForeignKey(Ordered_Table, on_delete=models.CASCADE)
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order for {self.table} at {self.order_time}"