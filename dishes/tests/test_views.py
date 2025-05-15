# dishes/tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from dishes.models import StandardCategory, RecommendationTag, Ingredient, Dish, IngrToDish 

class DishesViewsTest(TestCase):
    # Setup data for all test methods in the class
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # Create standard categories
        cls.cat1 = StandardCategory.objects.create(name="Appetizers", slug="appetizers", order=1)
        cls.cat2 = StandardCategory.objects.create(name="Main Courses", slug="main-courses", order=2)

        # Create recommendation tags
        cls.tag_veg = RecommendationTag.objects.create(name="Vegetarian", slug="veg")
        cls.tag_spicy = RecommendationTag.objects.create(name="Spicy", slug="spicy")
        cls.tag_new = RecommendationTag.objects.create(name="New Arrival", slug="new")

        # Create ingredients
        cls.ing_tomato = Ingredient.objects.create(name="Tomato")
        cls.ing_cheese = Ingredient.objects.create(name="Cheese")
        cls.ing_chili = Ingredient.objects.create(name="Chili")

        # Create dishes
        cls.dish1 = Dish.objects.create(
            name="Caprese Salad", standard_category=cls.cat1, price=Decimal("300.00"),
            is_vegetarian=True, description="Fresh tomatoes and mozzarella"
        )
        # Add tags to dish
        cls.dish1.recommendation_tags.add(cls.tag_veg, cls.tag_new)
        # Add ingredients to dish via join model
        IngrToDish.objects.create(dish=cls.dish1, ingredient=cls.ing_tomato, quantity=150, unit="g")
        IngrToDish.objects.create(dish=cls.dish1, ingredient=cls.ing_cheese, quantity=100, unit="g")

        cls.dish2 = Dish.objects.create(
            name="Pasta Carbonara", standard_category=cls.cat2, price=Decimal("450.00"),
            description="Classic Italian pasta"
        )
        # No specific tags for this one initially

        cls.dish3 = Dish.objects.create(
            name="Tom Yum", standard_category=cls.cat2, price=Decimal("550.00"),
            is_spicy=True, is_vegetarian=False, description="Spicy Thai soup"
        )
        cls.dish3.recommendation_tags.add(cls.tag_spicy)
        IngrToDish.objects.create(dish=cls.dish3, ingredient=cls.ing_chili, quantity=2, unit="pcs")

        cls.dish4 = Dish.objects.create(
            name="Vegetable Salad", standard_category=cls.cat1, price=Decimal("250.00"),
            is_vegetarian=True, is_spicy=False, description="Light vegetable salad"
        )
        cls.dish4.recommendation_tags.add(cls.tag_veg)

    # Test accessing an existing dish detail page
    def test_dish_detail_view_exists(self):
        url = reverse('dishes:dish_detail', args=[self.dish1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dish_detail.html')
        self.assertContains(response, self.dish1.name)
        # Check ingredient presence on the detail page
        self.assertContains(response, self.ing_tomato.name)
        # Check if the correct dish object is in the context
        self.assertEqual(response.context['dish'], self.dish1)

    # Test accessing a non-existent dish detail page
    def test_dish_detail_view_not_exists(self):
        # Use an ID that does not exist
        url = reverse('dishes:dish_detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # Test the dishes list view without any filters
    def test_dishes_view_no_filters(self):
        url = reverse('dishes:dishes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dishes.html')
        # Check if dishes list is in context
        self.assertIn('dishes', response.context)
        # Check if all dishes are returned
        self.assertEqual(len(response.context['dishes']), 4)
        # Check if filter options are in context
        self.assertIn('standard_categories', response.context)
        self.assertIn('recommendation_tags', response.context)
        self.assertIn(self.cat1, response.context['standard_categories'])
        self.assertIn(self.tag_veg, response.context['recommendation_tags'])

    # Test the dishes view with search filter
    def test_dishes_view_search_filter(self):
        url = reverse('dishes:dishes')
        # Search by dish name
        response = self.client.get(url, {'search': 'Caprese'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dishes']), 1)
        self.assertEqual(response.context['dishes'][0], self.dish1)
        # Check if search query is in context
        self.assertEqual(response.context['search_query'], 'Caprese')

        # Search by ingredient name
        response_ing = self.client.get(url, {'search': 'Chili'})
        self.assertEqual(response_ing.status_code, 200)
        # Check if the dish containing the ingredient is returned
        self.assertIn(self.dish3, response_ing.context['dishes'])

        # Search by category name
        response_cat = self.client.get(url, {'search': 'Main'})
        self.assertEqual(response_cat.status_code, 200)
        self.assertIn(self.dish2, response_cat.context['dishes'])
        self.assertIn(self.dish3, response_cat.context['dishes'])

        # Search by recommendation tag name
        response_tag = self.client.get(url, {'search': 'New Arrival'})
        self.assertEqual(response_tag.status_code, 200)
        self.assertIn(self.dish1, response_tag.context['dishes'])

    # Test the dishes view with category filter
    def test_dishes_view_category_filter(self):
        url = reverse('dishes:dishes')
        # Filter by Appetizers category ID
        response = self.client.get(url, {'standard_category': self.cat1.pk})
        self.assertEqual(response.status_code, 200)
        # Check if only dishes from the category are returned
        self.assertEqual(len(response.context['dishes']), 2) # dish1, dish4
        self.assertIn(self.dish1, response.context['dishes'])
        self.assertIn(self.dish4, response.context['dishes'])
        # Check if selected category ID is in context
        self.assertEqual(response.context['selected_standard_category_ids'], [str(self.cat1.pk)])

    # Test the dishes view with recommendation tag filter
    def test_dishes_view_recommendation_tag_filter(self):
        url = reverse('dishes:dishes')
        # Filter by Vegetarian tag ID
        response = self.client.get(url, {'recommendation_tag': self.tag_veg.pk})
        self.assertEqual(response.status_code, 200)
        # Check if only dishes with the tag are returned
        self.assertEqual(len(response.context['dishes']), 2) # dish1, dish4
        self.assertIn(self.dish1, response.context['dishes'])
        self.assertIn(self.dish4, response.context['dishes'])
        # Check if selected tag ID is in context
        self.assertEqual(response.context['selected_tag_ids'], [str(self.tag_veg.pk)])

    # Test the dishes view with vegetarian boolean filter
    def test_dishes_view_vegetarian_filter(self):
        url = reverse('dishes:dishes')
        # Filter by is_vegetarian=True
        response = self.client.get(url, {'vegetarian': 'on'})
        self.assertEqual(response.status_code, 200)
        # Check if only vegetarian dishes are returned
        self.assertEqual(len(response.context['dishes']), 2) # dish1, dish4
        self.assertIn(self.dish1, response.context['dishes'])
        self.assertIn(self.dish4, response.context['dishes'])
        # Check if filter state is in context
        self.assertTrue(response.context['filter_vegetarian'])

    # Test the dishes view with spicy boolean filter
    def test_dishes_view_spicy_filter(self):
        url = reverse('dishes:dishes')
        # Filter by is_spicy=True
        response = self.client.get(url, {'spicy': 'on'})
        self.assertEqual(response.status_code, 200)
        # Check if only spicy dishes are returned
        self.assertEqual(len(response.context['dishes']), 1)
        self.assertEqual(response.context['dishes'][0], self.dish3)
        # Check if filter state is in context
        self.assertTrue(response.context['filter_spicy'])

    # Test the dishes view with price range filter
    def test_dishes_view_price_filter(self):
        url = reverse('dishes:dishes')
        # Filter by minimum price
        response_min = self.client.get(url, {'min_price': '350.00'})
        self.assertEqual(response_min.status_code, 200)
        # Check dishes with price >= 350 (dish2, dish3)
        self.assertEqual(len(response_min.context['dishes']), 2)
        self.assertIn(self.dish2, response_min.context['dishes'])
        self.assertIn(self.dish3, response_min.context['dishes'])
        # Check if min price value is in context
        self.assertEqual(response_min.context['min_price_form'], '350.00')

        # Filter by maximum price
        response_max = self.client.get(url, {'max_price': '400.00'})
        self.assertEqual(response_max.status_code, 200)
        # Check dishes with price <= 400 (dish1, dish4)
        self.assertEqual(len(response_max.context['dishes']), 2)
        self.assertIn(self.dish1, response_max.context['dishes'])
        self.assertIn(self.dish4, response_max.context['dishes'])
        # Check if max price value is in context
        self.assertEqual(response_max.context['max_price_form'], '400.00')

        # Filter by price range
        response_range = self.client.get(url, {'min_price': '280.00', 'max_price': '480.00'})
        self.assertEqual(response_range.status_code, 200)
        # Check dishes with price between 280 and 480 (dish1, dish2)
        self.assertEqual(len(response_range.context['dishes']), 2)
        self.assertIn(self.dish1, response_range.context['dishes'])
        self.assertIn(self.dish2, response_range.context['dishes'])
        # Check initial slider values in context
        self.assertEqual(float(response_range.context['price_slider_js_config']['initialMin']), 280.00)
        self.assertEqual(float(response_range.context['price_slider_js_config']['initialMax']), 480.00)

    # Test the dishes view with a combination of filters
    def test_dishes_view_combined_filters(self):
        url = reverse('dishes:dishes')
        # Vegetarian dishes in "Appetizers" category
        response = self.client.get(url, {
            'standard_category': self.cat1.pk,
            'vegetarian': 'on'
        })
        self.assertEqual(response.status_code, 200)
        # Check if only dishes matching both criteria are returned (dish1, dish4)
        self.assertEqual(len(response.context['dishes']), 2)
        self.assertIn(self.dish1, response.context['dishes'])
        self.assertIn(self.dish4, response.context['dishes'])

        # Spicy dishes with price > 500
        response_spicy_price = self.client.get(url, {
            'spicy': 'on',
            'min_price': '500.00'
        })
        self.assertEqual(response_spicy_price.status_code, 200)
        # Check if only dish3 is returned
        self.assertEqual(len(response_spicy_price.context['dishes']), 1)
        self.assertEqual(response_spicy_price.context['dishes'][0], self.dish3)

    # Test the context data for the price slider when no filters are applied
    def test_dishes_price_slider_context(self):
        url = reverse('dishes:dishes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        price_config = response.context['price_slider_js_config']
        # Check overall min/max based on existing dishes
        self.assertAlmostEqual(float(price_config['overallMin']), float(self.dish4.price)) # dish4 has min price
        self.assertAlmostEqual(float(price_config['overallMax']), float(self.dish3.price)) # dish3 has max price
        # Initial values should match overall min/max without filters
        self.assertAlmostEqual(float(price_config['initialMin']), float(self.dish4.price))
        self.assertAlmostEqual(float(price_config['initialMax']), float(self.dish3.price))

        # Test with applied price filters
        response_filtered = self.client.get(url, {'min_price': '300', 'max_price': '500'})
        price_config_filtered = response_filtered.context['price_slider_js_config']
        # Initial values should reflect applied filters
        self.assertAlmostEqual(float(price_config_filtered['initialMin']), 300.00)
        self.assertAlmostEqual(float(price_config_filtered['initialMax']), 500.00)
        # Overall values should remain based on all dishes
        self.assertAlmostEqual(float(price_config_filtered['overallMin']), float(self.dish4.price))
        self.assertAlmostEqual(float(price_config_filtered['overallMax']), float(self.dish3.price))

    # Test price slider context when no dishes exist
    def test_dishes_price_slider_edge_cases_no_dishes(self):
        # Delete all dishes
        Dish.objects.all().delete()
        url = reverse('dishes:dishes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        price_config = response.context['price_slider_js_config']
        # Check default overall and initial values when no dishes
        self.assertAlmostEqual(float(price_config['overallMin']), 0.0)
        self.assertAlmostEqual(float(price_config['overallMax']), 1000.0) # Default max if no dishes
        self.assertAlmostEqual(float(price_config['initialMin']), 0.0)
        self.assertAlmostEqual(float(price_config['initialMax']), 1000.0)

    # Test price slider context when only one dish exists
    def test_dishes_price_slider_one_dish_same_price(self):
        # Clean up existing data to isolate this test case
        Dish.objects.all().delete()
        Ingredient.objects.all().delete()
        RecommendationTag.objects.all().delete()
        StandardCategory.objects.all().delete()

        # Create a minimal setup with one dish
        cat_temp = StandardCategory.objects.create(name="Temp", slug="temp")
        Dish.objects.create(name="Single Dish", standard_category=cat_temp, price=Decimal("50.00"))

        url = reverse('dishes:dishes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        price_config = response.context['price_slider_js_config']

        # Overall min and initial min should be the dish price
        self.assertAlmostEqual(float(price_config['overallMin']), 50.00)
        self.assertAlmostEqual(float(price_config['initialMin']), 50.00)
        # Overall max and initial max should be handled as a range if min==max
        self.assertAlmostEqual(float(price_config['overallMax']), 150.00) # Default range adjustment
        self.assertAlmostEqual(float(price_config['initialMax']), 150.00)