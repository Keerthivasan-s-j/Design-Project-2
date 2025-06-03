from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.user_logout, name="logout"),
    path('about/', views.about, name="about"),
    path('shop/', views.shop, name="shop"),
    path('contact/', views.contact, name="contact"),
    path('product/<int:id>/', views.product, name="product"),
    path('cart/', views.cart, name="cart"),
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name="remove_from_cart"),
    path('charging_hub/', views.charging_hub, name="charging_hub"),
    path('shipping/', views.shipping, name="shipping"),
    path('paymentsuccess/', views.paymentsuccess, name="paymentsuccess"),
    path('deliverydashboard/', views.deliverydashboard, name="deliverydashboard"),
]