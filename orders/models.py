from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Used by 2 classes, hence defined outside
LARGE_REGULAR = 'LREG'
SMALL_REGULAR = 'SREG'
LARGE_SICILIAN = 'LSIC'
SMALL_SICILIAN = 'SSIC'
SIZESTYLE_CHOICES = ( (LARGE_REGULAR, 'Large Regular'), (SMALL_REGULAR, 'Small Regular'), (LARGE_SICILIAN, 'Large Sicilian'), (SMALL_SICILIAN, 'Small Sicilian'),)

# Create your models here.
class PizzaOrder(models.Model):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pizzza_item_id")
  sizestyle = models.CharField(max_length=4, choices=SIZESTYLE_CHOICES, default=SMALL_REGULAR)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
  # null=true unnecessary for CharField since always '' stored? Also when ForeignKey?
  topping_1 = models.ForeignKey(Toppings, on_delete=models.DO_NOTHING, related_name="topping_1", blank=True, null=True)
  topping_2 = models.ForeignKey(Toppings, on_delete=models.DO_NOTHING, related_name="topping_2", blank=True, null=True)
  topping_3 = models.ForeignKey(Toppings, on_delete=models.DO_NOTHING, related_name="topping_3", blank=True, null=True)
  topping_4 = models.ForeignKey(Toppings, on_delete=models.DO_NOTHING, related_name="topping_4", blank=True, null=True)
  topping_5 = models.ForeignKey(Toppings, on_delete=models.DO_NOTHING, related_name="topping_5", blank=True, null=True)

  #strmeth

class PizzaPrice(models.Model):
  sizestyle = models.CharField(max_length=4, choices=SIZESTYLE_CHOICES, default=SMALL_REGULAR)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
  price = models.DecimalField(max_digits=6, decimal_places=2)

class SubPrice(models.Model):
  price_category = models.AutoField(primary_key=True)
  price_large = models.DecimalField(max_digits=6, decimal_places=2)
  price_small = models.DecimalField(max_digits=6, decimal_places=2)

class SubOrder(models.Model):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="sub_item_id")
  LARGE = 'L'
  SMALL = 'S'
  SIZE_CHOICES = ( (SMALL, 'Small'), (LARGE, 'Large'),)
  size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=SMALL)
  extra_count = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
  MUSHIES = 'M'
  PEPPERS = 'P'
  ONIONS = 'O'
  XTRCHEESE = 'C'
  EXTRA_CHOICES = ((MUSHIES, 'Mushrooms'),(PEPPERS, 'Peppers'),(ONIONS, 'Onions'),(XTRCHEESE, 'Extra Cheese'),)
  extra_1 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  extra_2 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  extra_3 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  extra_4 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  name = models.ForeignKey(Sub, on_delete=DO_NOTHING, related_name="sub_name")

class Sub(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
  price_category = models.ForeignKey(SubPrice, on_delete.DO_NOTHING, related_name="price_category")


class Order(models.Model):
  order_id = models.AutoField(primary_key=True)
  customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="active_customer")#can ditch rel name
  time = models.DateTimeField()
  total = models.DecimalField(max_digits=7, decimal_places=2)

class Item(models.Model):
  item_id = models.AutoField(primary_key=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")

# populate with all pizza toppings
class Toppings(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
