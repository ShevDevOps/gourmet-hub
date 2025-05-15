# dishes/tests/test_models.py
from django.test import TestCase
from django.db import IntegrityError
from django.utils.text import slugify
from decimal import Decimal

from dishes.models import StandardCategory, RecommendationTag, Ingredient, Dish, IngrToDish

# Test cases for the StandardCategory model
class StandardCategoryModelTest(TestCase):
    # Test creating a StandardCategory instance
    def test_create_standard_category(self):
        category = StandardCategory.objects.create(name="Main Courses", slug="main-courses", order=1)
        self.assertEqual(category.name, "Main Courses")
        self.assertEqual(category.slug, "main-courses")
        self.assertEqual(category.order, 1)
        self.assertEqual(str(category), "Main Courses")
        # Test verbose names and ordering defined in Meta
        self.assertEqual(StandardCategory._meta.verbose_name, "Standard Category")
        self.assertEqual(StandardCategory._meta.verbose_name_plural, "Standard Categories")
        self.assertEqual(StandardCategory._meta.ordering, ['order', 'name'])

    # Test the uniqueness constraint on the 'name' field
    def test_standard_category_name_unique(self):
        StandardCategory.objects.create(name="Appetizers", slug="appetizers")
        # Attempting to create another category with the same name should raise IntegrityError
        with self.assertRaises(IntegrityError):
            StandardCategory.objects.create(name="Appetizers", slug="appetizers-2")

    # Test the uniqueness constraint on the 'slug' field
    def test_standard_category_slug_unique(self):
        StandardCategory.objects.create(name="Drinks", slug="drinks")
        # Attempting to create another category with the same slug should raise IntegrityError
        with self.assertRaises(IntegrityError):
            StandardCategory.objects.create(name="Drinks-2", slug="drinks")

# Test cases for the RecommendationTag model
class RecommendationTagModelTest(TestCase):
    # Test creating a RecommendationTag instance
    def test_create_recommendation_tag(self):
        tag = RecommendationTag.objects.create(name="Spicy", slug="spicy")
        self.assertEqual(tag.name, "Spicy")
        self.assertEqual(tag.slug, "spicy")
        self.assertEqual(str(tag), "Spicy")
        # Test verbose names and ordering defined in Meta
        self.assertEqual(RecommendationTag._meta.verbose_name, "Recommendation Tag")
        self.assertEqual(RecommendationTag._meta.verbose_name_plural, "Recommendation Tags")
        self.assertEqual(RecommendationTag._meta.ordering, ['name'])

    # Test the uniqueness constraint on the 'name' field
    def test_recommendation_tag_name_unique(self):
        RecommendationTag.objects.create(name="For Kids", slug="for-kids")
        # Attempting to create another tag with the same name should raise IntegrityError
        with self.assertRaises(IntegrityError):
            RecommendationTag.objects.create(name="For Kids", slug="for-kids-2")

    # Test the uniqueness constraint on the 'slug' field
    def test_recommendation_tag_slug_unique(self):
        RecommendationTag.objects.create(name="Bestseller", slug="bestseller")
        # Attempting to create another tag with the same slug should raise IntegrityError
        with self.assertRaises(IntegrityError):
            RecommendationTag.objects.create(name="Bestseller-2", slug="bestseller")

# Test cases for the Ingredient model
class IngredientModelTest(TestCase):
    # Test creating an Ingredient instance
    def test_create_ingredient(self):
        ingredient = Ingredient.objects.create(name="Tomato")
        self.assertEqual(ingredient.name, "Tomato")
        self.assertEqual(str(ingredient), "Tomato")
        # Test verbose names and ordering defined in Meta
        self.assertEqual(Ingredient._meta.verbose_name, "Ingredient")
        self.assertEqual(Ingredient._meta.verbose_name_plural, "Ingredients")
        self.assertEqual(Ingredient._meta.ordering, ['name'])

    # Test the uniqueness constraint on the 'name' field
    def test_ingredient_name_unique(self):
        Ingredient.objects.create(name="Cucumber")
        # Attempting to create another ingredient with the same name should raise IntegrityError
        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name="Cucumber")

# Test cases for the Dish model
class DishModelTest(TestCase):
    # Setup data for Dish model tests
    @classmethod
    def setUpTestData(cls):
        cls.category = StandardCategory.objects.create(name="Soups", slug="soups", order=1)
        cls.tag1 = RecommendationTag.objects.create(name="Vegetarian", slug="vegetarian")
        cls.tag2 = RecommendationTag.objects.create(name="New Arrival", slug="new-arrival")
        cls.ingredient1 = Ingredient.objects.create(name="Potato")
        cls.ingredient2 = Ingredient.objects.create(name="Carrot")

    # Test creating a Dish instance
    def test_create_dish(self):
        dish = Dish.objects.create(
            standard_category=self.category,
            name="Borscht",
            description="Classic Ukrainian borscht", # Description can remain specific
            price=Decimal("150.00"),
            is_vegetarian=True,
            is_spicy=False
        )
        # Add recommendation tags to the dish
        dish.recommendation_tags.add(self.tag1, self.tag2)
        # Ingredients are linked via IngrToDish, tested separately

        self.assertEqual(dish.name, "Borscht")
        self.assertEqual(str(dish), "Borscht")
        self.assertEqual(dish.standard_category, self.category)
        self.assertEqual(dish.price, Decimal("150.00"))
        self.assertTrue(dish.is_vegetarian)
        self.assertFalse(dish.is_spicy)
        # Check that tags were added correctly
        self.assertIn(self.tag1, dish.recommendation_tags.all())
        self.assertIn(self.tag2, dish.recommendation_tags.all())
        # Test verbose names and ordering defined in Meta
        self.assertEqual(Dish._meta.verbose_name, "Dish")
        self.assertEqual(Dish._meta.verbose_name_plural, "Dishes")
        self.assertEqual(Dish._meta.ordering, ['standard_category__order', 'standard_category__name', 'name'])

    # Test the nullable behavior of the standard_category field
    def test_dish_standard_category_nullable(self):
        # standard_category is nullable due to on_delete=models.SET_NULL and null=True
        # blank=False means it's required in forms/admin, but can be programmatically set to None
        dish = Dish.objects.create(
            standard_category=None,
            name="Test Dish without Category",
            price=Decimal("100.00")
        )
        self.assertIsNone(dish.standard_category)

# Test cases for the IngrToDish model (Many-to-Many intermediary model)
class IngrToDishModelTest(TestCase):
    # Setup data for IngrToDish model tests
    @classmethod
    def setUpTestData(cls):
        cls.category = StandardCategory.objects.create(name="Salads", slug="salads")
        cls.dish = Dish.objects.create(standard_category=cls.category, name="Caesar Salad", price=Decimal("250.00"))
        cls.ingredient = Ingredient.objects.create(name="Chicken")

    # Test creating an IngrToDish instance
    def test_create_ingr_to_dish(self):
        ingr_to_dish = IngrToDish.objects.create(
            dish=self.dish,
            ingredient=self.ingredient,
            quantity=Decimal("100.00"),
            unit="g"
        )
        self.assertEqual(ingr_to_dish.dish, self.dish)
        self.assertEqual(ingr_to_dish.ingredient, self.ingredient)
        self.assertEqual(ingr_to_dish.quantity, Decimal("100.00"))
        self.assertEqual(ingr_to_dish.unit, "g")
        # Test string representation
        self.assertEqual(str(ingr_to_dish), f"{self.ingredient.name} for {self.dish.name}")
        # Test verbose names and unique_together defined in Meta
        self.assertEqual(IngrToDish._meta.verbose_name, "Ingredient in Dish")
        self.assertEqual(IngrToDish._meta.verbose_name_plural, "Ingredients in Dishes")
        # Check the unique_together constraint definition
        self.assertEqual(IngrToDish._meta.unique_together, (('dish', 'ingredient'),))

    # Test the unique_together constraint on (dish, ingredient)
    def test_ingr_to_dish_unique_together(self):
        # Create the first instance
        IngrToDish.objects.create(dish=self.dish, ingredient=self.ingredient, quantity=Decimal("50"), unit="g")
        # Attempting to create another instance with the same dish and ingredient should raise IntegrityError
        with self.assertRaises(IntegrityError):
            IngrToDish.objects.create(dish=self.dish, ingredient=self.ingredient, quantity=Decimal("75"), unit="g")