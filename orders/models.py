from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

# Used by 2 classes, hence defined outside
LARGE_REGULAR = 'LREG'
SMALL_REGULAR = 'SREG'
LARGE_SICILIAN = 'LSIC'
SMALL_SICILIAN = 'SSIC'
SIZESTYLE_CHOICES = ( (LARGE_REGULAR, 'Large Regular'), (SMALL_REGULAR, 'Small Regular'), (LARGE_SICILIAN, 'Large Sicilian'), (SMALL_SICILIAN, 'Small Sicilian'),)

class Order(models.Model):
  order_id = models.AutoField(primary_key=True)
  #https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
  customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="active_customer")#can ditch rel name
  time = models.DateTimeField()
  total = models.DecimalField(max_digits=7, decimal_places=2)

  def __str__(self):
    return f"Order {self.order_id}, customer: {self.customer}. Total: ${self.total} - {self.time}"

class Item(models.Model):
  item_id = models.AutoField(primary_key=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="to_order_id")

  def __str__(self):
    return f"Item {self.item_id} in order {self.order_id}. Price ${self.price}"

class PastaSalad(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"{self.name}, price: ${self.price}"

class Platter(models.Model):
  name = models.CharField(max_length=64, primary_key=True)

  def __str__(self):
    return f"{self.name}"

# populate with all pizza toppings
class Topping(models.Model):
  name = models.CharField(max_length=64, primary_key=True)

  def __str__(self):
    return f"{self.name}"

class PizzaPrice(models.Model):
  sizestyle = models.CharField(max_length=4, choices=SIZESTYLE_CHOICES, default=SMALL_REGULAR)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
  price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"Price for {self.sizestyle} pizza with {self.topping_count} toppings: ${self.price}"


class SubPrice(models.Model):
  price_category = models.AutoField(primary_key=True)
  price_large = models.DecimalField(max_digits=6, decimal_places=2)
  price_small = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

  def __str__(self):
    return f"Sub price category {self.price_category}: Large ${self.price_large}, Small ${self.price_small}"

class Sub(models.Model):
  name = models.CharField(max_length=64, primary_key=True)
  price_category = models.ForeignKey(SubPrice, on_delete=models.DO_NOTHING, related_name="sub_price_category")

  def __str__(self):
    return f"{self.name}, Price Category: {self.price_category}"

class PizzaOrder(models.Model):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pizzza_item_id")
  sizestyle = models.CharField(max_length=4, choices=SIZESTYLE_CHOICES, default=SMALL_REGULAR)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
  # null=true unnecessary for CharField since always '' stored? Also when ForeignKey?
  topping_1 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_1", blank=True, null=True)
  topping_2 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_2", blank=True, null=True)
  topping_3 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_3", blank=True, null=True)
  topping_4 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_4", blank=True, null=True)
  topping_5 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_5", blank=True, null=True)

  def __str__(self):
    toppings = []
    for i in range (topping_count):
      str = "topping_"+i
      toppings.append(str)
    return f"Pizza Order: Item {self.item_id}, Size & Style: {self.sizestyle}, Toppings: {self.topping_count}: {toppings}"


class PlatterPrice(models.Model):
  name = models.ForeignKey(Platter, on_delete=models.CASCADE, primary_key=True, related_name="platter_name")
  price_large = models.DecimalField(max_digits=6, decimal_places=2)
  price_small = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"{self.name} price: Large ${self.price_large}, Small ${self.price_small}"

class PlatterOrder(models.Model):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="platter_item_id")
  name = models.ForeignKey(Platter, on_delete=models.DO_NOTHING)
  LARGE = 'L'
  SMALL = 'S'
  SIZE_CHOICES = ( (SMALL, 'Small'), (LARGE, 'Large'),)
  size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=SMALL)

  def __str__(self):
    return f"Platter Order: Item {self.item_id}, {self.name}, size: {self.size}"

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
  name = models.ForeignKey(Sub, on_delete=models.DO_NOTHING, related_name="sub_name")

  def __str__(self):
    extras = []
    for i in range(extra_count):
      str = "extra_"+i
      extras.append(str)
    return f"Sub Order: Item {self.item_id}, {self.name}, size: {self.size}. {self.extra_count} Extras: {extras}"

class PastaSaladOrder(models.Model):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pastasalad_item_id")
  name = models.ForeignKey(PastaSalad, on_delete=models.DO_NOTHING, related_name="pastasalad_name")

  def __str__(self):
    return f"Pasta/Salad Order: Item {self.item_id}, {self.name}"
