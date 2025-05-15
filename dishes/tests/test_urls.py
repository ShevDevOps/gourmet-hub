# dishes/tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dishes.views import dishes, dish_detail

# Test URL routing for the dishes app
class DishesUrlsTest(SimpleTestCase):

    # Test if the 'dishes' URL resolves to the correct view function
    def test_dishes_url_resolves(self):
        url = reverse('dishes:dishes')
        self.assertEqual(resolve(url).func, dishes)

    # Test if the 'dish_detail' URL resolves to the correct view function
    def test_dish_detail_url_resolves(self):
        # For `resolve`, you need to pass arguments expected by the URL pattern
        # '1' is an example dish_id
        url = reverse('dishes:dish_detail', args=[1])
        self.assertEqual(resolve(url).func, dish_detail)