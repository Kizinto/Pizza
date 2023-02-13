from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.CharField(max_length=4, null=False)
    description = models.CharField(max_length=500)
    image = models.ImageField(blank=True, upload_to='pizza/')

    def __str__(self):
        return self.name


class Customer(models.Model):
    userid = models.CharField(max_length=10)
    mobileno = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.userid
