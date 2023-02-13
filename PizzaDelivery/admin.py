from django.contrib import admin
from . import models

class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

admin.site.register(models.Pizza, PizzaAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username', 'mobileno', 'email']

admin.site.register(models.Customer, CustomerAdmin)
