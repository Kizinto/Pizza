from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models
from OrderHandeling.models import Cart
from PizzaDelivery import forms

# **************************** Login & Logout ********************************


def staffLoginView(request):
    return render(request, "staff/staffLogin.html")


def staffHomepage(request):
    if request.user.is_authenticated:
        order_taken = models.AdminOrder.objects.filter(status="order_taken")
        cancel_orders = models.AdminOrder.objects.filter(status="order_cancelled")
        delivered_orders = models.AdminOrder.objects.filter(status="order_delivery_in_progress")
        completed_orders = models.AdminOrder.objects.filter(status="order_completed")
        contact = models.Contact.objects.all()

        order_count = len(order_taken)
        pizza_count = models.Pizza.objects.all().count()
        cancel_order_count = len(cancel_orders)
        delivering_items = len(delivered_orders)
        completed_orders_count = len(completed_orders)
        review_count = models.Review.objects.all().count()
        contact_count = len(contact)

        contextlib = {
            'order_count': order_count, 'pizza_count': pizza_count, 'cancel_order_count': cancel_order_count,
            'delivering_items': delivering_items, 'completed_orders_count': completed_orders_count,
            'review_count': review_count, 'contact_count':contact_count,
        }

        return render(request, "staff/main/staffHomepage.html", context=contextlib)
    else:
        messages.add_message(request, messages.ERROR, "Login Required")
        return redirect('staffLogin')


def authenticateStaff(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.groups.filter(name="Staff").exists():
            login(request, user)
            return redirect('staffHomepage')
        
        else:
            messages.add_message(request, messages.ERROR, "User Not Permitted")
            return redirect('staffLogin')

    else:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('staffLogin')


def logoutStaff(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout Successfully")
    return redirect('staffLogin')

# ***************************************************************************

# ************************** Contact *******************************


def contact(request):
    if request.user.is_authenticated:
        orders = Cart.objects.filter(user=request.user, is_paid=False)
        order_count = len(orders)
        if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            msg = request.POST['msg']

            try:
                mobile = int(phone)
                contact = models.Contact(name=name, email=email, phone=phone, message=msg)
                contact.save()
                messages.success(request, "Message Sent Successfully. We will be replying by mail.")
                return redirect('contact')

            except ValueError:
                messages.error(request, "Enter a Valid Mobile Number")
                return redirect('contact')

        contextlib = {
            'order_count': order_count,
        }
        return render(request, 'customer/contact.html', context=contextlib)

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['msg']

        try:
            mobile = int(phone)
            contact = models.Contact(name=name, email=email, phone=phone, message=msg)
            contact.save()
            messages.success(request, "Message Sent Successfully. We will be replying by mail.")
            return redirect('contact')

        except ValueError:
            messages.error(request, "Enter a Valid Mobile Number")
            return redirect('contact')

    return render(request, 'customer/contact.html')


def contactList(request):
    contact_list = models.Contact.objects.all()
    cotact_count = len(contact_list)
    contextlib = {
        'contact_list': contact_list,
        'contact_count': cotact_count,
    }
    return render(request, 'staff/main/contact.html', context=contextlib)


def deleteContact(request, contact_id):
    contact = get_object_or_404(models.Contact, pk=contact_id)
    contact.delete()
    return redirect('contact_list')

# ***************************************************************************

# *************************** Pizza Operations ******************************


def addPizza(request):
    if request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            form = forms.PizzaForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                price = form.cleaned_data.get("price")
                description = form.cleaned_data.get("description")
                img = form.cleaned_data.get("image")
                obj = models.Pizza.objects.create(
                    name=name,
                    price=price,
                    description=description,
                    image=img
                )
                obj.save()
                return redirect('viewPizza')
        else:
            form = forms.PizzaForm()
        context['form'] = form
        return render(request, "pizza/addForm.html", context)
    else:
        messages.add_message(request, messages.ERROR, "Login Required")
        return redirect('staffLogin')


def viewPizza(request):
    if request.user.is_authenticated:
        pizzas = models.Pizza.objects.all()
        return render(request, 'pizza/pizzaList.html', {'pizzas': pizzas})
    else:
        messages.add_message(request, messages.ERROR, "Login Required")
        return redirect('staffLogin')


def operationsPizza(request, pizza_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('delete'):
                pizza = get_object_or_404(models.Pizza, pk=pizza_id)
                pizza.delete()
                return redirect('viewPizza')

            if request.POST.get('update'):
                pizza = get_object_or_404(models.Pizza, pk=pizza_id)
                return render(request, 'pizza/updatePizza.html', {'pizza_id': pizza_id, 'pizza': pizza})
    else:
        messages.add_message(request, messages.ERROR, "Login Required")
        return redirect('staffLogin')


def updatePizza(request, pizza_id):
    if request.user.is_authenticated:
        pizza = get_object_or_404(models.Pizza, pk=pizza_id)
        pizza.name = request.POST['name']
        pizza.price = request.POST['price']
        pizza.description = request.POST['description']
        pizza.save()
        return redirect('viewPizza')
    else:
        messages.add_message(request, messages.ERROR, "Login Required")
        return redirect('staffLogin')


# ************************************************************************

# *********************** Order Management *******************************

def orderHistory(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, is_paid=False)
        order_count = len(cart_item)
        try:
            orders = models.AdminOrder.objects.filter(user=request.user)
            count = len(orders)

            contextlib = {
                'orders': orders,
                'order_len': count,
                'order_count': order_count
            }
            return render(request, 'customer/order_history.html', context=contextlib)

        except Exception as e:
            print(e)
            return redirect('home')

    else:
        return redirect('login')


def orderTracking(request):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user, is_paid=False)
        order_count = len(cart_item)
        if request.method == "POST":
            order_id = request.POST['order_id']

            try:
                order_int_id = int(order_id)
                try:
                    order = get_object_or_404(models.AdminOrder, order_id=order_id)
                    contextlib = {
                        'order': order,
                        'order_count':order_count,
                    }
                    return render(request, 'customer/order_tracking.html', context=contextlib)

                except Exception as e:
                    print(e)
                    messages.error(request, "Order ID not found")
                    return redirect('order_tracking')

            except ValueError:
                messages.error(request, "Invalid Order ID")
                return redirect('order_tracking')

        contextlib = {
            'order_count': order_count,
        }
        return render(request, 'customer/order_tracking_form.html', context=contextlib)

    else:
        if request.method == "POST":
            order_id = request.POST['order_id']

            try:
                order_int_id = int(order_id)
                try:
                    order = get_object_or_404(models.AdminOrder, order_id=order_id)
                    contextlib = {
                        'order': order,
                    }
                    return render(request, 'customer/order_tracking.html', context=contextlib)

                except Exception as e:
                    print(e)
                    messages.error(request, "Order ID not found")
                    return redirect('order_tracking')

            except ValueError:
                messages.error(request, "Invalid Order ID")
                return redirect('order_tracking')
        return render(request, 'customer/order_tracking_form.html')


def orderList(request):
    order_list = models.AdminOrder.objects.all()
    order_count = len(order_list)
    try:
        contextlib = {
            'orders': order_list,
            'order_count': order_count,
        }
        return render(request, 'staff/main/orders.html', context=contextlib)

    except Exception as e:
        return HttpResponse(e)


def statusUpdate(request, order_id):
    if request.method == "POST":
        try:
            if 'update' in request.POST:
                order_status = get_object_or_404(models.AdminOrder, order_id=order_id)
                contextlib = {
                    'order_status': order_status,
                    'order_id': order_id
                }

                return render(request, 'staff/main/order_status.html', context=contextlib)

            if 'delete' in request.POST:
                order = get_object_or_404(models.AdminOrder, order_id=order_id)
                order.delete()
                return redirect('orders')

        except Exception as e:
            return HttpResponse(e)


def orderStatusUpdate(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(models.AdminOrder, order_id=order_id)
        cart = Cart.objects.filter(order_id=order_id)

        order_status = request.POST['order_status']
        for cart_obj in cart:
            cart_obj.order_status = order_status
            cart_obj.save()

        order.status = order_status
        order.save()
        return redirect('orders')


def orderCancel(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            order_id = request.POST['order_id']
            name = request.POST['name']
            account_no = request.POST['account_no']
            email = request.POST['email']
            mobile = request.POST['mobile_no']

            try:
                valid_acc = int(account_no)
                valid_mobile = int(mobile)
                valid_order = int(order_id)

                try:
                    order = get_object_or_404(models.AdminOrder, order_id=order_id)
                    order.status = 'order_cancelled'
                    order.save()

                    cancel_order = models.CancelOrder(order=order, name=name, account_no=account_no, email=email,
                                                      mobile_no=mobile, is_returned=False)
                    cancel_order.save()
                    messages.success(request, "Order Cancelled Succesfully.")
                    return redirect('order_cancel')

                except Exception as e:
                    print(e)
                    messages.error(request, "Order Not Found. Please Enter Valid Order ID.")
                    return redirect('order_cancel')

            except ValueError:
                messages.error(request, "Please Enter Numbers in Number Inputs.")
                return redirect('order_cancel')

        else:
            cart_item = Cart.objects.filter(user=request.user, is_paid=False)
            order_count = len(cart_item)
            contextlib = {
                'order_count':order_count,
            }
            return render(request, 'payment/order_cancel_form.html', context=contextlib)

    if request.method == "POST":
        order_id = request.POST['order_id']
        name = request.POST['name']
        account_no = request.POST['account_no']
        email = request.POST['email']
        mobile = request.POST['mobile_no']

        order = get_object_or_404(models.AdminOrder, order_id=order_id)
        order.status = 'order_cancelled'
        order.save()

        cancel_order = models.CancelOrder(order=order, name=name, account_no=account_no, email=email,
                                          mobile_no=mobile, is_returned=False)
        cancel_order.save()
        return redirect('order_cancel')

    else:
        return render(request, 'payment/order_cancel_form.html')


def cancelRequests(request):
    orders = models.CancelOrder.objects.all()
    cancel_count = len(orders)
    contextlib = {
        'orders': orders,
        'cancel_count': cancel_count,
    }
    return render(request, 'staff/main/order_cancel_request.html', context=contextlib)


def deleteCancelRequest(request, order_id):
    if 'update' in request.POST:
        order = get_object_or_404(models.CancelOrder, pk=order_id)
        order.is_returned = True
        order.save()
        return redirect('order_cancel_request_list')

    if 'delete' in request.POST:
        order = get_object_or_404(models.CancelOrder, pk=order_id)
        main_order = get_object_or_404(models.AdminOrder, order_id=order.order.order_id)
        main_order.status = 'order_deleted'
        main_order.save()
        order.delete()
        return redirect('order_cancel_request_list')


# **********************************************************************

# ********************** Customer Review ********************************
def review(request):
    if request.user.is_authenticated:
            cart_item = Cart.objects.filter(user=request.user, is_paid=False)
            order_count = len(cart_item)
            if request.method == "POST":
                rating_star = request.POST['ratings']
                feedback = request.POST['feedback']
                rating = 0
                if rating_star == "star1":
                    rating = 5

                elif rating_star == "star2":
                    rating = 4

                elif rating_star == "star3":
                    rating = 3

                elif rating_star == "star4":
                    rating = 2

                elif rating_star == "star5":
                    rating = 1

                try:
                    feedback = models.Review(user=request.user, ratings=rating, feedback=feedback)
                    feedback.save()
                    messages.success(request, 'Feedback Sent Successfully')
                    return redirect('home')

                except Exception as e:
                    print(e)
                    return redirect('review')

            contextlib = {
                'order_count':order_count,
            }
            return render(request, 'payment/order_success.html', context=contextlib)

    if request.method == "POST":
        rating_star = request.POST['ratings']
        feedback = request.POST['feedback']
        rating = 0
        if rating_star == "star1":
            rating = 5

        elif rating_star == "star2":
            rating = 4

        elif rating_star == "star3":
            rating = 3

        elif rating_star == "star4":
            rating = 2

        elif rating_star == "star5":
            rating = 1

        try:
            feedback = models.Review(user=request.user, ratings=rating, feedback=feedback)
            feedback.save()
            messages.success(request, 'Feedback Sent Successfully')
            return redirect('home')

        except Exception as e:
            print(e)
            return redirect('review')
    return render(request, 'payment/order_success.html')


def reviewList(request):
    review_list = models.Review.objects.all()
    review_count = len(review_list)

    contextlib = {
        'reviews': review_list,
        'review_count': review_count,

    }
    return render(request, 'staff/main/reviews.html', context=contextlib)


def deleteReview(request, review_id):
    review = get_object_or_404(models.Review, pk=review_id)
    review.delete()
    return redirect('review_list')


# **************************************************************
