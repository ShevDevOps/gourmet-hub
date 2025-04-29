from django.db import models
from dishes.models import Dish

# Create your models here.
class Chef(models.Model): 
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chef_images/', null=True, blank=True)

class ChefToDish(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)