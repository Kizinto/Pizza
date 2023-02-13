from django.db import models
from django.contrib.auth.models import User
from PizzaDelivery.models import Pizza


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField()
    price = models.FloatField(max_length=5)
    total_price = models.FloatField(max_length=5)
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=7, default="", null=True)
    order_status = models.CharField(max_length=20, default="not_ordered", null=True)

    def __str__(self):
        return self.user.username


class Discount_Check(models.Model):
    username = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=6, null=False)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Discount_Code(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    discount = models.FloatField(max_length=3)

    def __str__(self):
        return self.title


class Checkout(models.Model):
    order_id = models.CharField(max_length=6, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)
    total_amount = models.FloatField(max_length=6)

    def __str__(self):
        return self.name
