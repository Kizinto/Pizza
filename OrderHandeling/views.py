from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from PizzaDelivery.models import Pizza
from StaffPanel.models import AdminOrder
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from deliveryproject import settings
import random, collections, datetime
from . import models


# **************************** Menu ********************************
def menu(request):
    pizzas = Pizza.objects.all()
    if request.user.is_authenticated:
        orders = models.Cart.objects.filter(user=request.user, is_paid=False)
        order_count = len(orders)
        context = {
            'pizzas': pizzas,
            'order_count':order_count,
        }
        return render(request, 'customer/menu.html', context)

    else:
        contextlib = {
            'pizzas': pizzas,
        }
        return render(request, 'customer/menu.html', contextlib)


# *******************************************************************************


# **************************** Cart ********************************
def cart_add(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    user = request.user
    order = models.Cart(user=user, pizza=pizza, quantity=1, price=pizza.price, total_price=pizza.price)
    order.save()
    return redirect('menu')


def item_clear(request, order_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)
    return redirect("cart_detail")


def item_increment(request, order_id):
    order = get_object_or_404(models.Cart, pk=order_id)
    order.quantity += 1
    order.total_price = order.quantity * order.price
    order.save()
    return redirect("cart_detail")


def item_decrement(request, order_id):
    order = get_object_or_404(models.Cart, pk=order_id)
    if order.quantity == 1:
        order.delete()
    else:
        order.quantity -= 1
        order.total_price = order.quantity * order.price
        order.save()
    return redirect("cart_detail")


def cart_clear(request):
    orders = models.Cart.objects.filter(user=request.user)
    for order in orders:
        order.delete()
    return redirect("cart_detail")


def cart_detail(request):
    orders = models.Cart.objects.filter(user=request.user, is_paid=False)
    order_count = len(orders)

    ''' Code for avoiding duplicates '''
    object_list_with_duplicates = [order.pizza for order in orders]
    duplicate_object_list = [item for item, count in collections.Counter(object_list_with_duplicates).items() if
                             count > 1]
    duplicate_dict = collections.Counter(object_list_with_duplicates)
    new_dict = dict()

    if len(duplicate_object_list) != 0:
        for item in duplicate_object_list:
            order = models.Cart.objects.filter(pizza=item)
            order.delete()

        for item, count in duplicate_dict.items():
            if count > 1:
                new_dict[item] = count

        for item, count in new_dict.items():
            order = models.Cart(user=request.user, pizza=item, quantity=count, price=item.price)
            order.total_price = int(order.quantity) * int(order.price)
            order.save()

        context = {
            'orders': orders,
            'order_count':order_count,
        }
        return render(request, 'customer/cart.html', context)

    else:
        context = {
            'orders': orders,
            'order_count': order_count,
        }
        return render(request, 'customer/cart.html', context)


# *******************************************************************************************


# **************************** Checkout ********************************

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        orders = models.Cart.objects.filter(user=request.user, is_paid=False)
        order_count = len(orders)
        random_num = random.sample(range(1000000, 5000000), 1)

        if request.method == 'POST':
            order_id = random_num[0]
            name = request.POST['name']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zip_code = request.POST['zip_code']
            phone = request.POST['phone']

            try:
                mobile = int(phone)

            except ValueError:
                messages.error(request, "Invalid Mobile Number")
                return redirect('checkout')

            try:
                pin = int(zip_code)

            except ValueError:
                messages.error(request, "Invalid Zip Code")
                return redirect('checkout')

            total_amount = 0
            for order in orders:
                order.order_id = order_id
                order.save()
                total_amount += order.total_price

            checkout_order = models.Checkout(order_id=order_id, user=request.user, name=name, address=address,
                                             city=city,
                                             state=state, zip_code=zip_code, phone=phone, total_amount=total_amount)
            checkout_order.save()

            razorpay_client =  client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            razorpay_order = razorpay_client.order.create(data=
                dict(amount=(checkout_order.total_amount * 100), currency='INR', receipt= "order_rcptid_11"))
            razorpay_order_id = razorpay_order['id']
            callback_url = 'handlerequest/'
            contextlib = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                'razorpay_amount': checkout_order.total_amount,
                'callback_url': callback_url,
                'total_amount': total_amount,
                'orders': orders,
                'order_count': order_count,
            }

            return render(request, 'payment/payment_page.html', context=contextlib)

        total_price = 0
        for order in orders:
            total_price += order.total_price

        contextlib = {
            'orders':orders,
            'Total':total_price,
            'order_count':order_count,
        }
        return render(request, 'customer/order_checkout.html', contextlib)


def go_back_to_cart(request):
    checkout = models.Checkout.objects.filter(user=request.user)
    checkout.delete()
    return redirect("cart_detail")


def discount(request):
    code = request.POST['code']
    user = request.user
    orders = models.Cart.objects.filter(user=request.user)
    try:
        code_object = get_object_or_404(models.Discount_Code, code=code)
        code_check = models.Discount_Check.objects.filter(username=user.username)
        code_applied = []

        if len(code_check) == 0:
            code_status = models.Discount_Check(username=user.username, code=code, is_applied=True)
            for order in orders:
                discount_amount = (order.total_price * code_object.discount) / 100
                order.total_price = order.total_price - discount_amount
                order.save()
            code_status.save()
            messages.success(request, 'Code Applied Successfully')
            return redirect('checkout')


        for code_user in code_check:
            if code_user.username == user.username:
                code_applied.append(code_user.code)

        for code_exist in range(len(code_applied)):
            if code_applied[code_exist] == code:
                messages.error(request, 'Code Already Applied')
                return redirect('checkout')

            else:
                code_status = models.Discount_Check(username=user.username, code=code, is_applied=True)
                for order in orders:
                    discount_amount = (order.total_price * code_object.discount) / 100
                    order.total_price = order.total_price - discount_amount
                    order.save()
                code_status.save()
                messages.success(request, 'Code Applied Successfully')
                return redirect('checkout')
        return redirect('checkout')
    except Exception as e:
        print(e)
        messages.error(request, "Code does not exist")
        return redirect('checkout')
# *******************************************************************************

# *********************** Payment Integration *****************************
@csrf_exempt
def handlerequest(request):
    unpaid_orders = models.Cart.objects.filter(user=request.user, is_paid=False)
    total_amount = 0
    for order in unpaid_orders:
        total_amount += order.total_price

    if request.method == "POST":
        try:
            now = datetime.datetime.now()

            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            for order in unpaid_orders:
                order.is_paid = True
                order.order_status = "order_taken"
                order.save()

            paid_orders = models.Cart.objects.filter(is_paid=True)
            pizzas = [x.pizza for x in paid_orders]
            admin_order = AdminOrder()
            admin_order.user = request.user
            admin_order.order_id = paid_orders[0].order_id
            admin_order.status = "order_taken"
            admin_order.timestamp = dt_string
            admin_order.total_amount = total_amount
            admin_order.save()
            for pizza in pizzas:
                admin_order.pizza.add(pizza)

            return redirect('review')

        except:
            return render(request, 'payment/order_failure.html')

    else:
        return HttpResponseBadRequest()

# *******************************************************************************
