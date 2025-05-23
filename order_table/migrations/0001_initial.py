# Generated by Django 5.1.2 on 2025-04-25 06:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('capacity', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ordered_Table',
            fields=[
                ('table_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='order_table.table')),
                ('Client_num', models.IntegerField()),
                ('Order_time', models.DateTimeField()),
                ('Client_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_table.client')),
            ],
            bases=('order_table.table',),
        ),
        migrations.CreateModel(
            name='DishToTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.dish')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_table.ordered_table')),
            ],
        ),
    ]
