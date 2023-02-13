from django.db import models
from PizzaDelivery.models import Pizza
from django.contrib.auth.models import User

Status_Choices = (
    ('not_ordered', 'not_ordered'),
    ('order_taken', 'order_taken'),
    ('order_deleted', 'order_deleted'),
    ('order_in_progress', 'order_in_progress'),
    ('order_delivery_in_progress', 'order_delivery_in_progress'),
    ('order_completed', 'order_completed'),
    ('order_cancelled', 'order_cancelled'),
)


class AdminOrder(models.Model):
    order_id = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pizza = models.ManyToManyField(Pizza)
    status = models.CharField(choices=Status_Choices, max_length=50, null=False, default="order_taken")
    total_amount = models.CharField(max_length=10, default=0, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    class Meta:
        unique_together = ['order_id']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    ratings = models.IntegerField(null=False)
    feedback = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.ratings)


class CancelOrder(models.Model):
    order = models.ForeignKey(AdminOrder, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=18, null=False)
    email = models.EmailField(max_length=100, null=False)
    mobile_no = models.CharField(max_length=10, null=True)
    is_returned = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name


class DeliveryOrder(models.Model):
    order_id = models.CharField(max_length=7)
    assigned_person = models.CharField(max_length=50)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.name
