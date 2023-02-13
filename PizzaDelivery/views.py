import math
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from OrderHandeling.models import Cart
from StaffPanel.models import Review
from . import models


def homepage(request):
    all_reviews = Review.objects.all()
    selected_reviews = []
    #for count in random.sample(range(len(all_reviews)), 6):
        #selected_reviews.append(all_reviews[count])

    total_reviews = len(all_reviews)
    one_star = 0
    two_star = 0
    three_star = 0
    four_star = 0
    five_star = 0
    average_star = 0

    for star in all_reviews:
        if star.ratings == 1:
            one_star += 1

        if star.ratings == 2:
            two_star += 1

        if star.ratings == 3:
            three_star += 1

        if star.ratings == 4:
            four_star += 1

        if star.ratings == 5:
            five_star += 1

    #average_star = (5 * one_star + 4 * two_star + 3 * three_star + 2 * two_star + one_star) / total_reviews
    average_star = math.ceil(average_star)

    if request.user.is_authenticated:
        orders = Cart.objects.filter(user=request.user, is_paid=False)
        order_count = len(orders)
        contextlib = {
            'reviews': selected_reviews,
            'total_reviews': total_reviews,
            'one_star': one_star,
            'two_star': two_star,
            'three_star': three_star,
            'four_star': four_star,
            'five_star': five_star,
            'average_star': average_star,
            'order_count':order_count,
        }
        return render(request, 'homepage/home.html', context=contextlib)

    else:
        contextlib = {
            'reviews': selected_reviews,
            'total_reviews': total_reviews,
            'one_star': one_star,
            'two_star': two_star,
            'three_star': three_star,
            'four_star': four_star,
            'five_star': five_star,
            'average_star': average_star,
        }
        return render(request, 'homepage/home.html', context=contextlib)


def signupUser(request):
    username = request.POST['username']
    password = request.POST['password']
    confirm_pass = request.POST['confirmation']
    mobileno = request.POST['mobileno']
    email = request.POST['email']

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username Already Exists")
        return redirect('login')

    if password != confirm_pass:
        messages.error(request, "Confirm password does not match!")
        return redirect('login')

    try:
        mobile = int(mobileno)

    except ValueError:
        messages.error(request, "Invalid Mobile Number")
        return redirect('login')

    else:
        User.objects.create_user(username=username, password=password).save()
        lastobject = len(User.objects.all()) - 1
        models.Customer(username=username, userid=User.objects.all()[lastobject].id, mobileno=mobileno,
                        email=email).save()
        customer = Group.objects.get(name='Customer')
        for user in User.objects.all():
            customer.user_set.add(user)
        messages.success(request, "User Created Successfully")
        return redirect('login')


def loginUser(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        if user is None:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'customer/login_signup.html')


def logoutCustomer(request):
    logout(request)
    return redirect('home')
