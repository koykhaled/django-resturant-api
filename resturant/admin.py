from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItems)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItems)