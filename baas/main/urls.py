from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name="landingpage"),
    path('signin/', views.signin, name="signin"),
    path('about/', views.about, name="about"),
    path('shop/', views.shop, name="shop"),
    path('contact/', views.contact, name="contact"),
]