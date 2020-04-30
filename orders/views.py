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

  if request.session["prebasket"]:
    pass # implement later if needed

  q_preseletion = {}
  preselection = []
  if request.method == 'POST':
  # "request.POST" returns an immutable QueryDict (sent as JSON) of items and amount pre-selected by user, hence copy() at end or dict()
    q_preselection = request.POST.dict()
    preselection = json.loads(q_preselection["preselection"])
    print("THIS IS THE POST REquest")
  #print("Q_PRESELECTION[preselection]: ", q_preselection["preselection"]) # prints OK
  if request.method == 'GET':
    q_preselection = request.GET.dict()
    print("THIS IS THE GET REQUEST - shouldn t come out now")
    return render(request, "pizza/prebasket.html")

  print("PRESELECTION THERE? ", preselection) # seems to come empty - hence key error , but also empty when localStorage not emppty(i.e. GET request)...weird
  # preselection is a list of dicts
  for item in preselection:
    # p is a dict
    print(f"PRINTING item:", item)
    print(f"PRINTING name:", item["name"])
    #dish = Dish.objects.get(pk=item["id"])
    price = ("%.2f" % float(item["price"]))
    total = ("%.2f" % float(item["total"]))
    item["price"] = price
    item["total"] = total
    print(f"Item is:", item)

  # store preselected items in session - check later if needed/utilised at all
  request.session["prebasket"] = preselection
  print(f"Request.session is:", request.session["prebasket"])
  context = {"items": preselection}
  print(f"Context is: ", context)
 # below not working
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
