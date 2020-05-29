from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect # same as above HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.template import loader
from django.core.mail import send_mail

from .forms import RegisterForm, SigninForm
from .models import *
import os, json, datetime

@login_required
def index(request):
  if request.method == 'POST':
    q_preselection = request.POST.dict()
    print("IS THERE ALREADY STH IN BASKET? ", q_preselection)

  e = SubOrder.EXTRA_CHOICES
  extras = [i[1] for i in e]
  toppings = []
  t = Topping.objects.all()
  for x in t:
    toppings.append(x.name)

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
    return render(request, "pizza/prebasket.html")

  if request.method == 'GET':
    # https://stackoverflow.com/questions/12165924/access-djangos-field-choices
    # that's to access tuples of choices
    e = SubOrder.EXTRA_CHOICES
    extras = [i[1] for i in e]
    # deliver sub [some info] to check against localStorage
    context = {"toppings": Topping.objects.all(),
                "extras": extras
                }
    return render(request, "pizza/prebasket.html", context)


@login_required
def basket(request):
  if request.method == "GET":
    return render(request, "pizza/confirmation.html")
  if request.method == "POST":

    pizza_orders = json.loads(request.POST["pizza_orders"]) # these are lists it seems
    sub_orders = json.loads(request.POST["sub_orders"])
    preselection = json.loads(request.POST["preselection"]) # dict retunred, but not sure if dict or list of dicts ? not sure..

    # create Order object
    order = Order(customer=request.user, time=datetime.datetime.now()) # somehow takes anna not bob
    order.save()
    total = 0

    for p in preselection: #{"amount": input.value, "id": input.id, "name": input.name, "size": size, "topping_count": topping_count, "price": price, "total": total, "dish_type": dish_type}
      d = Dish.objects.get(id=p["id"])

      total = total + float(d.price) * int(p["amount"])

      if p["dish_type"] == "PASTASALAD":
        dish = Dish.objects.get(id=p["id"])
        for x in range(int(p["amount"])):
          ps = PastaSaladOrder(order=order, dish=dish)
          ps.save()

      if p["dish_type"] == "PLATTER":
        dish = Dish.objects.get(id=p["id"])
        for x in range(int(p["amount"])):
          plo = PlatterOrder(order=order, dish=dish)
          plo.save()

    # 2. if pizza, create Pizza_order
    if (pizza_orders):
      for p in pizza_orders:
        #count toppings
        dish = Dish.objects.get(id=p["id"])
        print(len(p["toppings"]))

        # array needs to have length of 5 for each topping field, so fill blank toppings with None
        for x in range(5-len(p["toppings"])):
          p["toppings"].append(None)

        toppings = []
        for y in range(len(p["toppings"])):
          try: # better to write: if p["toppings"][y] != None: ### else: ### ?
            toppings.append(Topping.objects.get(name=p["toppings"][y]))
          except:
            toppings.append(None)

        po = PizzaOrder(dish=dish, order=order, topping_1=toppings[0], topping_2=toppings[1], topping_3=toppings[2], topping_4=toppings[3], topping_5=toppings[4])
        po.save()

    #    if sub, create Sub_order
    if (sub_orders):
      for s in sub_orders:
        dish = Dish.objects.get(id=s["id"])
        total = total + 0.5*len(s["extras"])
        price = float(dish.price) + 0.5*len(s["extras"])

        # fill empty fields with none
        for x in range(4-len(s["extras"])):
          s["extras"].append(None)

        so = SubOrder(dish=dish, order=order, extra_1=s["extras"][0], extra_2=s["extras"][1], extra_3=s["extras"][2], extra_4=s["extras"][3], price = price)
        so.save()

    # 4. calculate total
    print(f"TOTAL FINAL:", "%.2f" % total)
    # 5. save total in order
    order.total = "%.2f" % total
    order.save()

    # save order ID in session
    request.session['order_id'] = order.order_id
    # reset email_sent to False, so in next step, when custoemr submits order, he gets a confirmation email (in case he palces >1 orders)
    request.session['email_sent'] = False

  # Always return an HttpResponseRedirect after successfully dealing wiht POST data. Prevents from being posted twice if user hits back/refresh
  return HttpResponseRedirect(reverse('confirmation')) #HttpResponse(template.render(context, request))

@login_required
def confirmation(request, order_id=None):

  # if url called without parameter (i.e. from basket url as a result of a customer order)
  if order_id is None:
    order = Order.objects.get(pk=request.session['order_id'])
    title = "Step 3: Confirmation"
    email = request.user.email

    # only send email once, this will prevent a sending out of emails each time browser i refreshed
    if request.session['email_sent'] == False:
      send_mail('Order confirmation',
      'Your Pizza & Food Order ID %s has been placed. The total is $%s' % (order.order_id, order.total),
      'cs50pizza@gmail.com',
      [email],
      fail_silently=False,)
      print("CONF EMAIL SENT")
      request.session['email_sent'] = True


  # if url is called by staff member with parameter to fetch order info
  else:
    order = Order.objects.get(pk=order_id)
    title = "Order Info"
    email = None

  # query every DISHOrder belonging to order - then list in context
  pizzas = PizzaOrder.objects.filter(order=order.order_id)
  subs = SubOrder.objects.filter(order=order.order_id)
  pastasalads = PastaSaladOrder.objects.filter(order=order.order_id)
  platters = PlatterOrder.objects.filter(order=order.order_id)

  template = loader.get_template('pizza/confirmation.html')

  context = {
  "title": title,
  "pizzas": pizzas,
  "subs": subs,
  "pastasalads": pastasalads,
  "platters": platters,
  "order": order,
  "email": email
  }
  return HttpResponse(template.render(context, request))

@login_required
@staff_member_required
def order_history(request):
  # "-" makes it descending (-time)
  orders = Order.objects.all().order_by('-time')
  context = {
    "title": "Order History",
    "orders": orders
  }

  return render(request, "pizza/order_history.html", context)


@login_required
def logout_view(request):
  logout(request)
  form = SigninForm()
  template = loader.get_template('pizza/signin.html')
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
