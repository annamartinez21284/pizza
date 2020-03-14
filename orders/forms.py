from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "First Name", 'autocomplete': "nope"}), label="First name", max_length=64, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Last Name", 'autocomplete': "new-password"}), label="Last name", max_length=64, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Email", 'autocomplete': "new-password"}), label="Email", max_length=132, required=True)
    password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Password"}))
    confirmation = forms.CharField(label="Confirmation", max_length=32, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Confirm"}))

    def clean(self):
      super().clean()
      # if I replace below with email=self.cleaned_data["email"] & enter invalid email => key error
      # get() will not do that in case the dict entry isn't there & will return None
      # handle email format validation in JS - faster
      email = self.cleaned_data.get("email")
      if User.objects.filter(username=email).exists():
        raise forms.ValidationError(u'Email "%s" is already in use.' % email)

      password = self.cleaned_data["password"]
      confirmation = self.cleaned_data["confirmation"]
      if password != confirmation:
          raise forms.ValidationError("Password and confirmation do not match!")


class SigninForm(forms.Form):
  email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Email", 'autocomplete': "new-password"}), label="Email", max_length=132)
  password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Password"}))

  def clean(self):
    super().clean()
    email = self.cleaned_data.get("email")
    if not User.objects.filter(username=email).exists():
      raise forms.ValidationError(u'Email "%s" not found. Have you registered?' %email)

    # authentiacate user / password
