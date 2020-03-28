from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # same as above HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import RegisterForm, SigninForm
from .models import *

#TODO: Logout link in index.html, JS email vaildation

# Create your views here.
@login_required
def index(request):
  subs = Sub.objects.select_related('price_caegory')
  context = {
  # problem: SM and reg always have to be cheaper than sicilian...
  "0top": PizzaPrice.objects.filter(Q(topping_count=0)).order_by('price'),
  "1top": PizzaPrice.objects.filter(Q(topping_count=1)).order_by('price'),
  "2top": PizzaPrice.objects.filter(Q(topping_count=2)).order_by('price'),
  "3top": PizzaPrice.objects.filter(Q(topping_count=3)).order_by('price'),
  "5top": PizzaPrice.objects.filter(Q(topping_count=5)).order_by('price'),
  "toppings": Topping.objects.all(),
  "subs": Sub.objects.select_related('price_category'),
  "pastasalads": PastaSalad.objects.all(),
  "platters": Platter.objects.all()
  }
  return render(request, "pizza/index.html", context)

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
        msg = "Invalid creddentials"
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
