# https://stackoverflow.com/questions/17901341/django-how-to-make-a-variable-available-to-all-templates
# THIS CONTEXT CAN BE USED GLOBALLY IN ALL TEMPLATES NOW

def customer_processor(request):
 customer = request.user
 return {'customer': customer}
