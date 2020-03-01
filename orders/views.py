from django.http import HttpResponse #, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import RegisterForm, SigninForm

# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

def register(request):
  return render(request, "pizza/register.html")

def register_client(request):
  if request.method == "POST":
    form = RegisterForm(request.POST)
    if form.is_valid():
      # cleaned_data is a dict
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      print(f"PASSWORD VISIBLE?? : {password}")
      user = User.objects.create_user(email, password, email)
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.save()

  else:
    form = RegisterForm()
    print("IS THIS COMING OUT?")
    print(form.is_bound)

  return render(request, "pizza/register.html", {'form': form})
