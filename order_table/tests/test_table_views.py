from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from order_table.models import Table, Ordered_Table
from datetime import date

class OrderTableViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(capacity=4)
        self.table.is_available = True
        self.table.save()

    def test_order_table_url_requires_login(self):
        response = self.client.get(reverse('order_table'))
        self.assertEqual(response.status_code, 302)  # Перенаправлення на логін

    def test_order_table_get_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order_table'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')
        self.assertIn('tables', response.context)

    def test_order_table_post_success(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('order_table'), {
            'table_id': self.table.id,
            'people_count': 2,
            'date': date.today()
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        # Перевіряємо, що замовлення створено для User
        order = Ordered_Table.objects.filter(Client_Id=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.Client_num, 2)
        self.assertEqual(order.capacity, self.table.capacity)

    def test_order_table_post_exceeds_capacity(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('order_table'), {
            'table_id': self.table.id,
            'people_count': 10,  # більше за capacity
            'date': date.today()
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Number of people exceeds table capacity.'}
        )