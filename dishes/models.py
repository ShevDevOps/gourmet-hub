from django.db import models
from django.utils.text import slugify 

class StandardCategory(models.Model):
    name = models.CharField("Standard Category Name", max_length=100, unique=True) 
    slug = models.SlugField("Slug", max_length=110, unique=True, editable=True, blank=False)
    description = models.TextField("Description", blank=True, null=True)
    order = models.PositiveIntegerField("Sort Order", default=0, db_index=True)

    class Meta:
        verbose_name = "Standard Category"
        verbose_name_plural = "Standard Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name 

class RecommendationTag(models.Model):
    name = models.CharField("Recommendation Tag Name", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=110, unique=True, editable=True, blank=False)
    description = models.TextField("Description", blank=True, null=True)

    class Meta:
        verbose_name = "Recommendation Tag"
        verbose_name_plural = "Recommendation Tags"
        ordering = ['name']

    def __str__(self):
        return self.name 

class Ingredient(models.Model):
    name = models.CharField("Ingredient Name", max_length=100, unique=True)
    description = models.TextField("Description", null=True, blank=True)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ['name']

    def __str__(self):
        return self.name

class Dish(models.Model):
    standard_category = models.ForeignKey(
        StandardCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='dishes',
        verbose_name="Standard Category"
    )
    recommendation_tags = models.ManyToManyField(
        RecommendationTag,
        blank=True,
        related_name='recommended_dishes',
        verbose_name="Recommendation Tags"
    )
    ingredients_list = models.ManyToManyField(
        'Ingredient',
        through='IngrToDish',
        blank=True,
        verbose_name="Ingredients"
    )
    name = models.CharField("Dish Name", max_length=100)
    description = models.TextField("Description", null=True, blank=True)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    image = models.ImageField("Image", upload_to='dish_images/', null=True, blank=True)
    is_vegetarian = models.BooleanField("Vegetarian", default=False)
    is_spicy = models.BooleanField("Spicy", default=False)

    class Meta:
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"
        ordering = ['standard_category__order', 'standard_category__name', 'name']

    def __str__(self):
        return self.name

class IngrToDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Dish")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingredient")
    quantity = models.DecimalField("Quantity", max_digits=10, decimal_places=2)
    unit = models.CharField("Unit", max_length=20, default='g') # e.g., 'g', 'ml', 'pcs'

    class Meta:
        verbose_name = "Ingredient in Dish"
        verbose_name_plural = "Ingredients in Dishes"
        unique_together = ('dish', 'ingredient')

    def __str__(self):
        return f"{self.ingredient.name} for {self.dish.name}"