from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Cart, CartItems, Notification, UserProfile, Order, OrderItem
from .data import indian_states
import urllib.parse

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("landingpage")
        
        return render(request, "main/signin.html", {"username": username})
    
    return render(request, "main/signin.html")

def send_bulk_notification(sender, message):
    delivery_boys = UserProfile.objects.filter(role='delivery')  # or use Group logic

    for profile in delivery_boys:
        Notification.objects.create(
            sender=sender,
            receiver=profile.user,
            message=message
        )

def user_logout(request):
    logout(request)
    return redirect("signin")

def user_logout(request):
    logout(request)
    return render(request, "main/signin.html")

@login_required(login_url='signin')
def landingpage(request):
    if request.method == "POST":
        search = request.POST.get("search")
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()[:3]
        search = ""

    context = {
        "products": products,
        "search" : search
    }

    if request.user.profile.role == "delivery":
        return redirect("deliverydashboard")
    
    return render(request, "main/landingpage.html", context)

@login_required(login_url='signin')
def deliverydashboard(request):
    user_profile = request.user.profile
    if user_profile.role != 'delivery':
        return redirect('landingpage')

    orders = Order.objects.all().order_by('-created_at')
    notifications = Notification.objects.filter(receiver = request.user).order_by('-created_at')
    context = {
        "notifications" : notifications,
        "orders" : orders
    }
    return render(request, "main/deliverydashboard.html", context)

@require_POST
@login_required(login_url='signin')
def start_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Optional: Only delivery users can start delivery
    if request.user.profile.role != 'delivery':
        return redirect('landingpage')

    # Update order status and assign delivery user
    order.status = 'Out for Delivery'
    order.assigned_to = request.user
    order.save()

    return redirect('deliverydashboard')


def about(request):
    return render(request, "main/about.html")

def shop(request):
    search = ""
    if request.method == "POST":
        form_name = request.POST.get("form_name")
        if (form_name == "search_form"):
            search = request.POST.get("search")
            products = Product.objects.filter(name__icontains=search)
        else:
            category = int(request.POST.get("category"))
            if (category == 0):
                products = Product.objects.all()
            else:
                products = Product.objects.filter(category = category)

    else:
        products = Product.objects.all()

    context = {
        "products": products,
        "search" : search
    }
    return render(request, "main/shop.html", context)

def contact(request):
    return render(request, "main/contact.html")

def product(request, id):
    product = Product.objects.get(id=id)
    context={
        "product_id" : id,
        "product" : product
    }
    return render(request, "main/product.html", context)

@login_required(login_url='signin')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    grand_total = sum(item.total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'grand_total': grand_total
    }
    return render(request, "main/cart.html", context)

def add_to_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_item, cart_item_created = CartItems.objects.get_or_create(cart=cart, product=product)

    if not cart_item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect("cart")

def remove_from_cart(request, id):
    product = get_object_or_404(Product, pk=id)
    cart, created = Cart.objects.get_or_create(user = request.user)
    cart_item = CartItems.objects.get(cart = cart, product  = product)
    if (cart_item.quantity > 1):
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


def charging_hub(request):
    embed_url = ""
    place = ""
    if request.method == "POST":
        place = request.POST.get("search")
        if place:
            search_query = f"{place} EV charging stations"
            encoded_query = urllib.parse.quote(search_query)
            embed_url = f"https://maps.google.com/maps?q={encoded_query}&output=embed"
    
    return render(request, "main/charging_hub.html", {"embed_url": embed_url, "place" : place})

@login_required(login_url='signin')
def bulk_shipping(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product')

    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zipCode')
        country = request.POST.get('country', 'India')
        phone = request.POST.get('phone')

        total_amount = sum(item.quantity * item.product.price for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            phone=phone,
            total_amount=Decimal(total_amount)
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        send_bulk_notification(sender=request.user, message=f"New bulk order placed (ID: {order.id})")
        return redirect('ordersuccessful')

    context = {
        "indian_states": indian_states,
        "cart_items": cart_items,
        "individually_ordered": False
    }
    return render(request, "main/shipping.html", context)


@login_required(login_url='signin')
def item_shipping(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get shipping form data
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zipCode')
        country = request.POST.get('country', 'India')
        phone = request.POST.get('phone')
        quantity = int(request.POST.get('quantity', 1))  # Allow quantity to be passed in form

        total_amount = Decimal(product.price) * quantity

        # Create Order
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            phone=phone,
            total_amount=total_amount
        )

        # Create OrderItem
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        # Notify delivery
        send_bulk_notification(sender=request.user, message=f"New single-product order placed (ID: {order.id})")

        return redirect('ordersuccessful')

    context = {
        "product": product,
        "indian_states": indian_states,
        "individually_ordered": True
    }
    return render(request, "main/shipping.html", context)

    # if request.method == "POST":
    #     return redirect("paymentsuccess")
    # context = {
    #     "indian_states" : indian_states
    # }
    # return render(request, "main/shipping.html", context)

@login_required(login_url='signin')
def order_success(request):
    return render(request, "main/ordersuccessful.html")

def paymentsuccess(request):
    return render(request, "main/paymentsuccess.html")

@login_required(login_url='signin')
def my_orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/myorders.html', {'orders': user_orders})