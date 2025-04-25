from django.db import models
from django.core.exceptions import ValidationError
from dishes.models import Dish

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Ordered_Table(Table):
    Client_Id = models.ForeignKey(Client, on_delete=models.CASCADE)
    Client_num = models.IntegerField()
    Order_time = models.DateTimeField()

    def clean(self):
        if self.capacity < self.Client_num:
            raise ValidationError("Client number exceeds table capacity.")
        super().clean()

    def __str__(self):
        return self.name
    
class DishToTable(models.Model):
    table = models.ForeignKey(Ordered_Table, on_delete=models.CASCADE)
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order for {self.table} at {self.order_time}"