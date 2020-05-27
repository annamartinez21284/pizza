from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
admin.site.register(Order)
admin.site.register(Dish)
#admin.site.register(Item)
#admin.site.register(PastaSalad)
#admin.site.register(Platter)
admin.site.register(Topping)
#admin.site.register(Pizza)
#admin.site.register(SubPrice)
#admin.site.register(Sub)
admin.site.register(PizzaOrder)
admin.site.register(PlatterOrder)
admin.site.register(SubOrder)
admin.site.register(PastaSaladOrder)
#admin.site.register(RegisterForm, SigninForm)
