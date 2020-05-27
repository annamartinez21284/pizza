# Generated by Django 2.0.3 on 2020-05-20 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20200520_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suborder',
            name='extra_1',
            field=models.CharField(blank=True, choices=[('M', 'Mushrooms'), ('P', 'Peppers'), ('O', 'Onions'), ('C', 'Extra Cheese')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='extra_2',
            field=models.CharField(blank=True, choices=[('M', 'Mushrooms'), ('P', 'Peppers'), ('O', 'Onions'), ('C', 'Extra Cheese')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='extra_3',
            field=models.CharField(blank=True, choices=[('M', 'Mushrooms'), ('P', 'Peppers'), ('O', 'Onions'), ('C', 'Extra Cheese')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='extra_4',
            field=models.CharField(blank=True, choices=[('M', 'Mushrooms'), ('P', 'Peppers'), ('O', 'Onions'), ('C', 'Extra Cheese')], max_length=1, null=True),
        ),
    ]
