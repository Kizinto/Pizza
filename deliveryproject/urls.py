from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from PizzaDelivery import views as customer_handeling
from OrderHandeling import views as order_handeling
from StaffPanel import views as staff_handeling

urlpatterns = [
               path('admin/', admin.site.urls),

               # ************************ Customer ******************************
               path('', customer_handeling.homepage, name="home"),
               path('home/signup/', customer_handeling.signupUser, name="signup"),
               path('home/login/', customer_handeling.loginUser, name="login"),
               path('home/logout/', customer_handeling.logoutCustomer, name="logout"),
               # ********************************************************************

               # ************************ Staff ******************************
               # ----------------------------- Main Staff -----------------------------
               path('staff/login/', staff_handeling.staffLoginView, name="staffLogin"),
               path('staff/authenticate/', staff_handeling.authenticateStaff, name="authenticate"),
               path('staff/home/', staff_handeling.staffHomepage, name="staffHomepage"),
               path('staff/addPizza/', staff_handeling.addPizza, name="addPizza"),
               path('staff/viewPizza/', staff_handeling.viewPizza, name="viewPizza"),
               path('staff/deletePizza/<int:pizza_id>/', staff_handeling.operationsPizza, name="deletePizza"),
               path('staff/updatePizza/<int:pizza_id>/', staff_handeling.updatePizza, name="updatePizza"),
               path('staff/orders/', staff_handeling.orderList, name="orders"),
               path('staff/orders/statusUpdate/<int:order_id>/', staff_handeling.statusUpdate, name="status_update"),
               path('staff/orders/updateStatus/<int:order_id>/', staff_handeling.orderStatusUpdate,
                  name="update_status_form"),
               path('order/cancel/', staff_handeling.orderCancel, name="order_cancel"),
               path('review/', staff_handeling.review, name="review"),
               path('review/list/', staff_handeling.reviewList, name="review_list"),
               path('review/delete/<int:review_id>/', staff_handeling.deleteReview, name="delete_review"),
               path('staff/logout/', staff_handeling.logoutStaff, name="staffLogout"),
               path('staff/contact/', staff_handeling.contactList, name="contact_list"),
               path('staff/contact/delete/<int:contact_id>', staff_handeling.deleteContact, name="delete_contact"),

               # ________________________Other Features _________________________________________
               path('order/tracking/', staff_handeling.orderTracking, name="order_tracking"),
               path('contact/', staff_handeling.contact, name="contact"),

               # ***********************************************************

               # ***************** Order Handling ***********************
               path('menu/', order_handeling.menu, name="menu"),

               # ----------------------------- Cart -----------------------
               path('cart/add/<int:pizza_id>/', order_handeling.cart_add, name='cart_add'),
               path('cart/item_clear/<int:order_id>/', order_handeling.item_clear, name='item_clear'),
               path('cart/item_increment/<int:order_id>/', order_handeling.item_increment, name='item_increment'),
               path('cart/item_decrement/<int:order_id>/', order_handeling.item_decrement, name='item_decrement'),
               path('cart/cart_clear/', order_handeling.cart_clear, name='cart_clear'),
               path('cart/cart-detail/', order_handeling.cart_detail, name='cart_detail'),

               # ----------------------------- Checkout -----------------------------
               path('checkout/', order_handeling.checkout, name='checkout'),
               path('checkout/clear/', order_handeling.go_back_to_cart, name="go_back_to_cart"),
               path('discount/', order_handeling.discount, name="discount"),
               path('checkout/handlerequest/', order_handeling.handlerequest, name="handlerequest"),

               # ----------------------------- Order History & Cancellation ---------------
               path('order_history/', staff_handeling.orderHistory, name="order_history"),
               path('order/cancel/request_list', staff_handeling.cancelRequests, name="order_cancel_request_list"),
               path('order/cancel/delete/<int:order_id>/', staff_handeling.deleteCancelRequest,
                  name="delete_cancel_request"),

               # *****************************************************************

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
