from django.contrib import admin
from OrderHandeling import models

admin.site.register(models.Cart)
admin.site.register(models.Checkout)
admin.site.register(models.Discount_Check)
admin.site.register(models.Discount_Code)