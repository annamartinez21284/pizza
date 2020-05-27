# Generated by Django 2.0.3 on 2020-05-20 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200520_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]