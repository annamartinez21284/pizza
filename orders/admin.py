from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(PastaSalad)
admin.site.register(Platter)
admin.site.register(Toppings)
admin.site.register(PizzaPrice)
admin.site.register(SubPrice)
admin.site.register(Sub)
admin.site.register(PizzaOrder)
admin.site.register(PlatterPrice)
admin.site.register(PlatterOrder)
admin.site.register(SubOrder)
admin.site.register(PastaSaladOrder)