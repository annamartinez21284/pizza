# Generated by Django 2.0.3 on 2020-05-27 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20200526_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suborder',
            name='extra_1',
            field=models.CharField(blank=True, choices=[('Mushrooms', 'Mushrooms'), ('Peppers', 'Peppers'), ('Onions', 'Onions'), ('Extra Cheese', 'Extra Cheese')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='extra_2',
            field=models.CharField(blank=True, choices=[('Mushrooms', 'Mushrooms'), ('Peppers', 'Peppers'), ('Onions', 'Onions'), ('Extra Cheese', 'Extra Cheese')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='extra_3',
            field=models.CharField(blank=True, choices=[('Mushrooms', 'Mushrooms'), ('Peppers', 'Peppers'), ('Onions', 'Onions'), ('Extra Cheese', 'Extra Cheese')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='suborder',
            name='extra_4',
            field=models.CharField(blank=True, choices=[('Mushrooms', 'Mushrooms'), ('Peppers', 'Peppers'), ('Onions', 'Onions'), ('Extra Cheese', 'Extra Cheese')], max_length=64, null=True),
        ),
    ]
