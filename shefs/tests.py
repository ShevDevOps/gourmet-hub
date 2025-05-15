import tempfile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Chef


TEMP_MEDIA_ROOT  = tempfile.mkdtemp()

class ChefModelTest(TestCase):
    def test_create_chef(self):
        
        chef = Chef.objects.create(name="Gordon Ramsay", description="Famous chef")
        self.assertEqual(str(chef.name), "Gordon Ramsay")

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ChefViewsTest(TestCase):
    def setUp(self):
        image_mock = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/jpeg'
        )
        self.chef = Chef.objects.create(name="Jamie Oliver", description="Another famous chef", image=image_mock)

    def test_shefs_list_view(self):
        response = self.client.get(reverse('shefs'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.chef.name)

    def test_shef_detail_view(self):
        response = self.client.get(reverse('shef_detail', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.chef.description)