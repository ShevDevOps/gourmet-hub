from django.test import TestCase
from django.contrib.auth.models import User
from order_table.models import Table, Ordered_Table, DishToTable
from dishes.models import Dish
from django.core.exceptions import ValidationError
from datetime import date

class TableModelTest(TestCase):
    def test_table_str_and_capacity(self):
        table = Table.objects.create(capacity=4)
        # Додаємо is_available вручну, якщо його немає в моделі
        table.is_available = True
        self.assertIn("Available", str(table))
        table.is_available = False
        self.assertIn("Not Available", str(table))
        self.assertEqual(table.capacity, 4)

class OrderedTableModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(capacity=4)
        self.table.is_available = True

    def test_ordered_table_create_and_str(self):
        order = Ordered_Table.objects.create(
            id=self.table.id,  # Наслідування PK від Table
            Client_Id=self.user,
            Client_num=2,
            Order_time=date.today(),
            capacity=self.table.capacity
        )
        self.assertEqual(order.Client_Id, self.user)
        self.assertEqual(order.Client_num, 2)
        self.assertEqual(str(order), f"Order {order.id} for {self.user} on {order.Order_time}")

    def test_ordered_table_clean_validation(self):
        order = Ordered_Table(
            id=self.table.id,
            Client_Id=self.user,
            Client_num=10,  # більше за capacity
            Order_time=date.today(),
            capacity=self.table.capacity
        )
        with self.assertRaises(ValidationError):
            order.clean()

class DishToTableModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(capacity=4)
        self.table.is_available = True
        self.order = Ordered_Table.objects.create(
            id=self.table.id,
            Client_Id=self.user,
            Client_num=2,
            Order_time=date.today(),
            capacity=self.table.capacity
        )
        self.dish = Dish.objects.create(
            name="Test Dish",
            price=10.0,
            description="Test"
        )

    def test_dish_to_table_str(self):
        dish_to_table = DishToTable.objects.create(table=self.order, Dish=self.dish)
        # Якщо у DishToTable немає поля order_time, видаліть його з f-рядка
        self.assertIn(str(self.order), str(dish_to_table))