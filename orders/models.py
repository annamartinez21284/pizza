from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings
#from model_utils.managers import InheritanceManager

# Used by >1 classes, hence defined outside
# LARGE_REGULAR = 'Large Regular'
# SMALL_REGULAR = 'Small Regular'
# LARGE_SICILIAN = 'Large Sicilian'
# SMALL_SICILIAN = 'Small Sicilian'
# SIZESTYLE_CHOICES = ( (LARGE_REGULAR, 'Large Regular'), (SMALL_REGULAR, 'Small Regular'), (LARGE_SICILIAN, 'Large Sicilian'), (SMALL_SICILIAN, 'Small Sicilian'),)

LARGE = 'L'
SMALL = 'S'
SIZE_CHOICES = ( (SMALL, 'Small'), (LARGE, 'Large'),)


class Dish(models.Model):
  name = models.CharField(max_length=64, blank=True) # blank makes name optional
  size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=SMALL, blank=True)
  price = models.DecimalField(max_digits=6, decimal_places=2, default=None)

  def __str__(self):
    return f"{self.name}, {self.size} - Price: ${self.price}"

class Order(models.Model):
  order_id = models.AutoField(primary_key=True)
  #https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
  customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="active_customer")#can ditch rel name
  time = models.DateTimeField()
  total = models.DecimalField(max_digits=7, decimal_places=2)

  def __str__(self):
    return f"Order {self.order_id}, customer: {self.customer}. Total: ${self.total} - {self.time}"

class Item(Dish):
  item_id = models.AutoField(primary_key=True)
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_item")
  #price = models.DecimalField(max_digits=6, decimal_places=2)
  order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="to_order_id")

  def __str__(self):
    return f"Item {self.item_id} in order {self.order_id}. Price ${self.price}"

class PastaSalad(Dish):
  #Dish.counter +=1
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_pastasalad")
  #name = models.CharField(max_length=64, primary_key=True)
  #price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"{self.name}, price: ${self.price}"


class Topping(models.Model):
  name = models.CharField(max_length=64, primary_key=True)

  def __str__(self):
    return f"{self.name}"

class Pizza(Dish):
  #Dish.counter +=1
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_pizza")
  REGULAR = 'REGULAR'
  SICILIAN = 'SICILIAN'
  STYLE_CHOICES = ( (REGULAR, 'Regular'), (SICILIAN, 'Sicilian'),)
  style = models.CharField(max_length=7, choices=STYLE_CHOICES, default=REGULAR)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
  #price = models.DecimalField(max_digits=6, decimal_places=2)

  def __str__(self):
    return f"Price for {self.size} {self.style} pizza with {self.topping_count} toppings: ${self.price}"


# class SubPrice(models.Model):
#   price_category = models.AutoField(primary_key=True)
#   price_large = models.DecimalField(max_digits=6, decimal_places=2)
#   price_small = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
#
#   def __str__(self):
#     return f"Sub price category {self.price_category}: Large ${self.price_large}, Small ${self.price_small}"

class Sub(Dish):
  #Dish.counter +=1
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_sub")
  #name = models.CharField(max_length=64, primary_key=True)
  #price_category = models.ForeignKey(SubPrice, on_delete=models.DO_NOTHING, related_name="sub_price_category")

  def __str__(self):
    return f"{self.name}, Price: ${self.price}"

class PizzaOrder(Pizza):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pizza_item_id")
  # sizestyle = models.CharField(max_length=4, choices=SIZESTYLE_CHOICES, default=SMALL_REGULAR)
  # # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  # topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
  # # null=true unnecessary for CharField since always '' stored? Also when ForeignKey?
  # topping_1 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_1", blank=True, null=True)
  # topping_2 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_2", blank=True, null=True)
  # topping_3 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_3", blank=True, null=True)
  # topping_4 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_4", blank=True, null=True)
  # topping_5 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_5", blank=True, null=True)

  def __str__(self):
    toppings = []
    for i in range (topping_count):
      str = "topping_"+i
      toppings.append(str)
    return f"Pizza Order: Item {self.item_id}, Size & Style: {self.size} {self.style}, Toppings: {self.topping_count}: {toppings}"


class Platter(Dish):
  #name = models.ForeignKey(Platter, on_delete=models.CASCADE, primary_key=True, related_name="platter_name")
  #Dish.counter +=1
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_platter")
  #name = models.CharField(max_length=64, primary_key=True)
  #price_large = models.DecimalField(max_digits=6, decimal_places=2, default=0)
  #price_small = models.DecimalField(max_digits=6, decimal_places=2, default=0)

  def __str__(self):
    return f"{self.name} price: Large ${self.price_large}, Small ${self.price_small}"

class PlatterOrder(Platter):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="platter_item_id")
  # name = models.ForeignKey(Platter, on_delete=models.DO_NOTHING)
  # LARGE = 'L'
  # SMALL = 'S'
  # SIZE_CHOICES = ( (SMALL, 'Small'), (LARGE, 'Large'),)
  # size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=SMALL)

  def __str__(self):
    return f"Platter Order: Item {self.item_id}, {self.name}, size: {self.size}"

class SubOrder(Sub):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="sub_item_id")
  # LARGE = 'L'
  # SMALL = 'S'
  # SIZE_CHOICES = ( (SMALL, 'Small'), (LARGE, 'Large'),)
  # size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=SMALL)
  extra_count = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
  MUSHIES = 'M'
  PEPPERS = 'P'
  ONIONS = 'O'
  XTRCHEESE = 'C'
  EXTRA_CHOICES = ((MUSHIES, 'Mushrooms'), (PEPPERS, 'Peppers'), (ONIONS, 'Onions'), (XTRCHEESE, 'Extra Cheese'),)
  extra_1 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  extra_2 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  extra_3 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  extra_4 = models.CharField(max_length=1,choices=EXTRA_CHOICES, blank=True)
  #name = models.ForeignKey(Sub, on_delete=models.DO_NOTHING, related_name="sub_name")

  def __str__(self):
    extras = []
    for i in range(extra_count):
      str = "extra_"+i
      extras.append(str)
    return f"Sub Order: Item {self.item_id}, {self.name}, size: {self.size}. {self.extra_count} Extras: {extras}"

class PastaSaladOrder(PastaSalad):
  item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pastasalad_item_id")
  #name = models.ForeignKey(PastaSalad, on_delete=models.DO_NOTHING, related_name="pastasalad_name")

  def __str__(self):
    return f"Pasta/Salad Order: Item {self.item_id}, {self.name}"
