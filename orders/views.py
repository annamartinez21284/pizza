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
import json

#TODO: Logout link in index.html, JS email vaildation

# Create your views here.
@login_required
def index(request):
  if request.method == 'POST':
    q_preselection = request.POST.dict()
    print("IS THERE ALREADY STH IN BASKET? ", q_preselection) # comes out empty

  cheese = Pizza.objects.filter(Q(topping_count=0)).order_by('price')
  for c in cheese:
    print("CHEESES cOME OUT AS:")
    print(c.size, c.style, c.topping_count)
  # create empty dict, populate w item_ID & quantity(0) and return as json.dumps to client (JS)

  context = {
  # problem: SM and reg always have to be cheaper than sicilian...
  "0top": Pizza.objects.filter(Q(topping_count=0)).order_by('price'),
  "1top": Pizza.objects.filter(Q(topping_count=1)).order_by('price'),
  "2top": Pizza.objects.filter(Q(topping_count=2)).order_by('price'),
  "3top": Pizza.objects.filter(Q(topping_count=3)).order_by('price'),
  "5top": Pizza.objects.filter(Q(topping_count=5)).order_by('price'),
  "toppings": Topping.objects.all(),
  "subs": Sub.objects.all(),
  "pastasalads": PastaSalad.objects.all(),
  "platters": Platter.objects.all()
  }
  return render(request, "pizza/index.html", context)

@login_required
def prebasket(request):
  q_preseletion = {}
  if request.method == 'POST':
  # below returns an immutable QueryDict (sent as JSON) of items and amount pre-selected by user, hence copy() at end or dict()
    q_preselection = request.POST.dict()
    print("THIS IS THE POST REquest")
  #print("Q_PRESELECTION[preselection]: ", q_preselection["preselection"]) # prints OK
  if request.method == 'GET':
    q_preselection = request.GET.dict()
    print("THIS IS THE GET REQUEST - shouldn t come out now")

  print("QPRESELECTION THERE? ", q_preselection) # seems to come empty - hence key error , but also empty when localStorage not emppty(i.e. GET request)...weird
  for key, value in q_preselection.items():
    print("PRINTING KEY AND VAL")
    print (key, value)

  #print("JSON LOADS: ", json.loads(q_preselection["preselection"]))

  # convert JSON to Python Dict with json.loads()
  preselection = json.loads(q_preselection["preselection"])
  try:
    del preselection[""]
    del preselection["csrfmiddlewaretoken"] # redundant now
  except KeyError:
    pass
  #preselection = qpreselection.dict()["preselection"]
  print(f"PRESELECTION NOX CONVERTED TO:", preselection)
  # declare empty list to add info to
  items = []
  # iterate thru menu items (ids) in user's selection
  for id in preselection:
    print(f"ID IS:", id)
    dish = Dish.objects.get(pk=id)
    print(f"Dish is:", dish)
    print(f"Class name is:", dish.__class__.__name__)
    item = {
    "id": dish.id,
    "name": dish.name,
    "size": dish.size,
    "price": ("%.2f" % float(dish.price)),
    "amount": preselection[id],
    "total": ("%.2f" % (int(preselection[id]) * float(dish.price)))
    }

    # if dish is a pizza - no obvs easy way to get object's child class in Django apparently
    try:
      item["style"] = dish.style
      item["topping_count"] = dish.topping_count
    except AttributeError:
      pass
    items.append(item)
    print(f"Item is:", item)
  # store preselected items in session - check later if needed/utilised at all
  request.session["prebasket"] = items
  print(f"Request.session is:", request.session["prebasket"])
  context = {"items": items}
  print(f"Context is: ", context)
  if request.is_ajax():
    print("Request is AJAX")
    html = render_to_string('pizza/prebasket.html', {'items': items})
    return HttpResponse(html)
  return render(request, "pizza/prebasket.html", context)

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
