# Generated by Django 2.0.3 on 2020-05-20 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20200520_0648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pizzaorder',
            old_name='order_id',
            new_name='order',
        ),
    ]