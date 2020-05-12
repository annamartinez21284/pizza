from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # same as above HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string

from .forms import RegisterForm, SigninForm
from .models import *
import json, datetime

#TODO: Logout link in index.html, JS email vaildation

# Create your views here.
@login_required
def index(request):
  if request.method == 'POST':
    q_preselection = request.POST.dict()
    print("IS THERE ALREADY STH IN BASKET? ", q_preselection)

  cheese = Dish.objects.filter(type="Pizza",topping_count=0).order_by('price')
  for c in cheese:
    print("CHEESES cOME OUT AS:")
    print(c.size, c.style, c.topping_count)

  e = SubOrder.EXTRA_CHOICES
  extras = [i[1] for i in e]
  toppings = []
  t = Topping.objects.all()
  for x in t:
    toppings.append(x.name)

  print(f"TOPPINGS ARE: ", toppings)

  context = {
  # problem: SM and reg always have to be cheaper than sicilian with current html design...
  "0top": Dish.objects.filter(topping_count=0, type="PIZZA").order_by('price'),
  "1top": Dish.objects.filter(topping_count=1, type="PIZZA").order_by('price'),
  "2top": Dish.objects.filter(topping_count=2, type="PIZZA").order_by('price'),
  "3top": Dish.objects.filter(topping_count=3, type="PIZZA").order_by('price'),
  "5top": Dish.objects.filter(topping_count=5, type="PIZZA").order_by('price'),
  "toppings": toppings,
  "subs": Dish.objects.filter(type="SUB"),
  "pastasalads": Dish.objects.filter(type="PASTASALAD"),
  "platters": Dish.objects.filter(type="PLATTER"),
  "extras": extras
  }

  return render(request, "pizza/index.html", context)

@login_required
def prebasket(request):

  if request.method == 'POST':
  # "request.POST" returns an immutable QueryDict (sent as JSON) of items and amount pre-selected by user, hence copy() at end or dict()
    print("THIS IS THE POST REquest- shouldn t come out now")
    return render(request, "pizza/prebasket.html")

  if request.method == 'GET':

    print("THIS IS THE GET REQUEST")
    # https://stackoverflow.com/questions/12165924/access-djangos-field-choices
    # that's to access tuples of choices
    e = SubOrder.EXTRA_CHOICES
    # i[1] gets 'index 1', i.e. the 2nd item from tuple list e ((M, 'Mushrooms', P, 'Peppers', etc)
    extras = [i[1] for i in e]
    # deliver sub [some info] to check against localStorage
    context = {"toppings": Topping.objects.all(),
                "extras": extras}
    return render(request, "pizza/prebasket.html", context)


@login_required
def basket(request, selection): # need to update path like path("<int:flight_id>", views.flight)
  pass


@login_required
def logout_view(request):
  logout(request)
  form = SigninForm()
  return render(request, "pizza/signin.html",  {'form': form})

def sign_in(request):
  if request.method == "POST":
    #creates a SigninForm instance and populates with data from request “binding data to the form” (it is now a bound form)
    form = SigninForm(request.POST)
    print(f"FORM SHOULD BE BOUND NOW? {form.is_bound}")

    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      print(f"Can probably see password? {password}")
      user = authenticate(username=email, password=password)
      if user is not None:
        login(request, user)
        return redirect(reverse('index')) # same as redirect('/')
      else:
        messages.error(request,'Invalid credentials.')
        # UGLY - fix here
        msg = "Invalid credentials"
        # https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/
        # reverse() method will be callled automatically by passing name of view?
        return render(request, 'pizza/signin.html', {'msg': msg})
  else:
    form = SigninForm()
    print("SIGNIN FORM SHOULD NOT BE BOUND NOW:")
    print(form.is_bound)

  return render(request, "pizza/signin.html", {'form': form})

def register_client(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    print("FORM SHOULD BE BOUND NOW?")
    print(form.is_bound)
    if form.is_valid():
      # cleaned_data is a dict
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      print(f"PASSWORD VISIBLE?? : {password}")
      # username = email address (user, email, password) is order of arguments
      user = User.objects.create_user(email, email, password)
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.save()
      return redirect('/')

  else:
    form = RegisterForm()
    print("FORM SHOULD NOT BE BOUND NOW:")
    print(form.is_bound)

  return render(request, "pizza/register.html", {'form': form})
