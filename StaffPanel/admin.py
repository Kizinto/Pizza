from django.contrib import admin
from . import models


class AdminOrderStatus(admin.ModelAdmin):
    list_display = ['order_id', 'status', 'timestamp']


class CancelOrderModel(admin.ModelAdmin):
    list_display = ['name', 'email', 'account_no', 'mobile_no', 'is_returned']


class DeliveryOrderModel(admin.ModelAdmin):
    list_display = ['order_id', 'assigned_person']

class ContactModel(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

admin.site.register(models.AdminOrder, AdminOrderStatus)
admin.site.register(models.Review)
admin.site.register(models.DeliveryOrder, DeliveryOrderModel)
admin.site.register(models.CancelOrder, CancelOrderModel)
admin.site.register(models.Contact, ContactModel)