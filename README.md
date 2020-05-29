# Project 3

Web Programming with Python and JavaScript

## Description

This is a food ordering app built on Django.
It is my submission of Project 3 of CS50W. Full details of usage/requirements at:
https://docs.cs50.net/ocw/web/projects/3/project3.html.

The main files containing my code/logic are (others are Django components, env variables, etc.):

* orders/views.py - all urls and backend / database logic based on Django models
* orders/models.py - ORM, all models for the database (available to clone with this repo)
* orders/forms.py - contains signin and register forms (use Django Forms)
* orders/static/pizza/order.js - processes customer selection client-side and builds form with preselected items for submission
* orders/static/pizza/prebasket.js - processes preselected form with client customization (extras) and submits order to server
* orders/static/pizza/outer.css - css for register and signin
* orders/static/pizza/inner.css - css for all other templates
* orders/templates/pizza/index.html - template with menu
* orders/templates/pizza/signin.html - sign in template
* orders/templates/pizza/register.html - register template
* orders/templates/pizza/prebasket.html - preselected basket
* orders/templates/pizza/confirmation.html - confirmation and order info template (for viewing order details)
* orders/templates/pizza/order_history.html - for staff members only
* orders/templates/pizza/innerlayout.html - base layout for forms after login
* orders/templates/pizza/outerlayout.html - base layout for register and signin

## Usage
1. Create a Python virtual environment:
    ```
    python3 -mvenv <virtual_env>
    ```
2. Install module dependencies:
    ```
    pip3 install -r requirements.txt
    ```
3. Clone Github repo:
    ```
    git clone https://github.com/annamartinez21284/pizza.git
    ```


4. Change into directory
    ```
    cd pizza
    ```

5. Create a .env file with email credentials, for example on a Gmail host (for app to send out order confirmation):
    ```
    EMAIL_HOST_USER = "example@gmail.com"
    EMAIL_HOST_PASSWORD = "Password"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ```
6. Admins can make changes to the database (orders, menu, users) via the Django admin interface(http://ip-address:port/admin/).
   If no database cloned from my repo, set up a superuser:
    ```
    python3 manage.py createsuperuser
    ```

## Limitations

This app is for learning purposes. Not intended for actual usage, no customer address stored, no order management, no payment system,
no password reset, no contact form, etc. implemented.
Design and interface very basic, I focused on functionality.
