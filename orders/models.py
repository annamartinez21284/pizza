from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings



class Dish(models.Model):
  name = models.CharField(max_length=64, blank=True) # blank makes name optional

  PIZZA = 'PIZZA'
  SUB = 'SUB'
  PASTASALAD = 'PASTASALAD'
  PLATTER = 'PLATTER'
  TYPE_CHOICES = ( (PIZZA, 'Pizza'), (SUB, 'Sub'), (PASTASALAD, 'PastaSalad'), (PLATTER, 'Platter') )
  type = models.CharField(max_length=64, choices=TYPE_CHOICES, blank=True)

  REGULAR = 'REGULAR'
  SICILIAN = 'SICILIAN'
  STYLE_CHOICES = ( (REGULAR, 'Regular'), (SICILIAN, 'Sicilian'),)
  style = models.CharField(max_length=64, choices=STYLE_CHOICES, blank=True)

  LARGE = 'L'
  SMALL = 'S'
  SIZE_CHOICES = ( (SMALL, 'Small'), (LARGE, 'Large'),)
  size = models.CharField(max_length=1, choices=SIZE_CHOICES, default=SMALL, blank=True)

  price = models.DecimalField(max_digits=6, decimal_places=2, default=None, null=True, blank=True)
  topping_count = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)], blank=True) #validators overwrite blank=True


  def __str__(self):
    return f"{self.name} {self.size} - Price: ${self.price}"

class Order(models.Model):
  order_id = models.AutoField(primary_key=True)
  #https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model
  customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="active_customer")#can ditch rel name?
  time = models.DateTimeField(auto_now_add=True)
  total = models.DecimalField(max_digits=7, decimal_places=2, default=0)
  #dish = models.ManyToManyField(Dish) # will allow to add many dishes to order -  ONLY 1 EACH! - not needed

  def __str__(self):
    time = self.time.strftime("%m/%d/%Y, %H:%M:%S")
    return f"Order ID: {self.order_id}, customer: {self.customer}. Time: {time}. Total: ${self.total}"


class Topping(models.Model):
  name = models.CharField(max_length=64, primary_key=True)

  def __str__(self):
    return f"{self.name}"

class PizzaOrder(models.Model):
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_pizza")
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pizza_to_order_id", default=None)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_1 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_1", blank=True, null=True)
  topping_2 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_2", blank=True, null=True)
  topping_3 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_3", blank=True, null=True)
  topping_4 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_4", blank=True, null=True)
  topping_5 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_5", blank=True, null=True)

  def __str__(self):
    toppings = list(filter(None, [self.topping_1, self.topping_2, self.topping_3, self.topping_4, self.topping_5]))
    for i in range (len(toppings)):
      toppings[i] = toppings[i].name
    t = ", ".join(toppings)
    if toppings:
      return f"{self.dish.name} {self.dish.style} {self.dish.size}, Toppings: {t}"
    else:
      return f"{self.dish.name} {self.dish.style} {self.dish.size}"


class PlatterOrder(models.Model):
  dish = models.ForeignKey(Dish, related_name="platter_dish_id", on_delete=models.DO_NOTHING)
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="platter_to_order_id")

  def __str__(self):
    return f"{self.dish.name} {self.dish.size}"

class SubOrder(models.Model):
  dish = models.ForeignKey(Dish, related_name="sub_dish_id", on_delete=models.DO_NOTHING)
  #item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="sub_item_id")
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="sub_to_order_id")
  #extra_count = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
  MUSHROOMS = 'Mushrooms'
  PEPPERS = 'Peppers'
  ONIONS = 'Onions'
  XTRCHEESE = 'Extra Cheese'
  EXTRA_CHOICES = ((MUSHROOMS, 'Mushrooms'), (PEPPERS, 'Peppers'), (ONIONS, 'Onions'), (XTRCHEESE, 'Extra Cheese'),)
  extra_1 = models.CharField(max_length=64, choices=EXTRA_CHOICES, blank=True, null=True)
  extra_2 = models.CharField(max_length=64, choices=EXTRA_CHOICES, blank=True, null=True)
  extra_3 = models.CharField(max_length=64, choices=EXTRA_CHOICES, blank=True, null=True)
  extra_4 = models.CharField(max_length=64, choices=EXTRA_CHOICES, blank=True, null=True)
  price = models.DecimalField(max_digits=6, decimal_places=2, default=None, null=True, blank=True)

  def __str__(self):
    extras = list(filter(None, [self.extra_1, self.extra_2, self.extra_3, self.extra_4]))
    e = ", ".join(extras)
    if extras:
      return f"{self.dish.name} {self.dish.size}, Extras: {e}"
    else:
      return f"{self.dish.name} {self.dish.size}"

class PastaSaladOrder(models.Model):
  dish = models.ForeignKey(Dish, related_name="pastasalad_dish_id", on_delete=models.DO_NOTHING)
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pastasalad_to_order_id")

  def __str__(self):
    return f"{self.dish.name}"
