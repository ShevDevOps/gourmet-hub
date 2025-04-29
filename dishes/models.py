from django.db import models

# Create your models here.

class Dish(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dish_images/', null=True, blank=True)

class Ingridient(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ingredient_images/', null=True, blank=True)

class IngrToDish(models.Model): 
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)