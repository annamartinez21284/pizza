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
  customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="active_customer")#can ditch rel name
  time = models.DateTimeField()
  total = models.DecimalField(max_digits=7, decimal_places=2)
  dish = models.ManyToManyField(Dish) # will allow to add many dishes to order

  def __str__(self):
    return f"Order {self.order_id}, customer: {self.customer}. Total: ${self.total} - {self.time}"

# class Item(models.Model):
#   item_id = models.AutoField(primary_key=True)
#   #dish = models.OneToOneField(Dish, on_delete=models.CASCADE, related_name="dish_id_item", parent_link=True)
#   #price = models.DecimalField(max_digits=6, decimal_places=2)
#   order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="to_order_id")
#
#   def __str__(self):
#     return f"Item {self.item_id} in order {self.order_id}. Price ${self.price}"

# class PastaSalad(Dish):
#   dish = models.OneToOneField(Dish, on_delete=models.CASCADE, related_name="dish_id_pastasalad", parent_link=True)
#
#   def __str__(self):
#     return f"{self.name}, price: ${self.price}"


class Topping(models.Model):
  name = models.CharField(max_length=64, primary_key=True)

  def __str__(self):
    return f"{self.name}"

class PizzaOrder(models.Model):
  dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_id_pizza")
  order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pizza_to_order_id", default=None)
  # need full_clean below? https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  topping_1 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_1", blank=True)
  topping_2 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_2", blank=True)
  topping_3 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_3", blank=True)
  topping_4 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_4", blank=True)
  topping_5 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_5", blank=True)

  def __str__(self):
    return f"{self.style} pizza with {self.topping_count} toppings"


# class Sub(Dish):
#   dish = models.OneToOneField(Dish, on_delete=models.CASCADE, related_name="dish_id_sub", parent_link=True)
#
#   def __str__(self):
#     return f"{self.name}, Size: ${self.size}, Price: ${self.price}"

# class PizzaOrder(models.Model):
#   pizza_id = models.ForeignKey(Pizza, related_name="pizza_dish_id", on_delete=models.DO_NOTHING)
#   # if only line below: django.db.utils.OperationalError: foreign key mismatchch - "orders_pizzaorder" referencing "orders_pizza"
#   #item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pizza_item_id")
#   order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pizza_order_id")
#   topping_1 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_1", blank=True)
#   topping_2 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_2", blank=True)
#   topping_3 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_3", blank=True)
#   topping_4 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_4", blank=True)
#   topping_5 = models.ForeignKey(Topping, on_delete=models.DO_NOTHING, related_name="topping_5", blank=True)
#
#   def __str__(self):
#
#     return f"Pizza Order: {self.order_id}, Size & Style: {self.size} {self.style}, Toppings: {self.topping_1}"


# class Platter(Dish):
#   dish = models.OneToOneField(Dish, on_delete=models.CASCADE, related_name="dish_id_platter", parent_link=True)
#
#   def __str__(self):
#     return f"{self.name} price: ${self.price}, size ${self.size}"
#
# class PlatterOrder(models.Model):
#   #item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="platter_item_id")
#   order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="platter_to_order_id")
#   platter_id = models.ForeignKey(Platter, related_name="platter_id")
#
#
#   def __str__(self):
#     p = Platter.objects.get(pk=platter_id)
#     return f"Platter Order: {self.order_id}, {p.name}, size: {p.size}"

class SubOrder(models.Model):
  dish_id = models.ForeignKey(Dish, related_name="sub_dish_id", on_delete=models.DO_NOTHING)
  #item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="sub_item_id")
  order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="sub_to_order_id")
  extra_count = models.IntegerField(default=0, validators=[MaxValueValidator(4), MinValueValidator(0)])
  MUSHIES = 'M'
  PEPPERS = 'P'
  ONIONS = 'O'
  XTRCHEESE = 'C'
  EXTRA_CHOICES = ((MUSHIES, 'Mushrooms'), (PEPPERS, 'Peppers'), (ONIONS, 'Onions'), (XTRCHEESE, 'Extra Cheese'),)
  extra_1 = models.CharField(max_length=1, choices=EXTRA_CHOICES, blank=True)
  extra_2 = models.CharField(max_length=1, choices=EXTRA_CHOICES, blank=True)
  extra_3 = models.CharField(max_length=1, choices=EXTRA_CHOICES, blank=True)
  extra_4 = models.CharField(max_length=1, choices=EXTRA_CHOICES, blank=True)

  def __str__(self):
    extras = []
    for i in range(extra_count):
      str = "extra_"+i
      extras.append(str)
    return f"Sub Order: {self.order_id}, {self.extra_count} Extras: {extras}"

# class PastaSaladOrder(models.Model):
#   order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pastasalad_to_order_id")
#   pastasalad_id = models.ForeignKey(PastaSalad, related_name="pastasalad_id")
#   #item_id = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, related_name="pastasalad_item_id")
#
#   def __str__(self):
#     ps = PastaSalad.objects.get(pk=pastasalad_id) # LET'S SEE IF THIS WORKS
#     return f"Pasta/Salad Order: {self.order_id}, {ps.name}"
