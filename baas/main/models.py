from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class UserProfile(models.Model):
    USER = 'user'
    DELIVERY = 'delivery'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (DELIVERY, 'Delivery'),
        (ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Product(models.Model):

    CATEGORY = [
        (1, 'EV Bike'),
        (2, 'EV Car'),
        (3, 'Accessories')
    ]

    DELEVERY_CHOISES = [
        ('free', "Free Delevery"),
        ('paid', "Paid Delevery"),
    ]

    name = models.CharField(verbose_name='Product Name', max_length=50)
    image = models.ImageField(verbose_name='Product Image', upload_to='images/')
    details = models.TextField(verbose_name='Details', default='Product detail')
    price = models.IntegerField(verbose_name='Product Price')
    category = models.IntegerField(verbose_name='Category', choices=CATEGORY)
    delevery_option = models.CharField(verbose_name='Delevery Option', max_length=10, choices=DELEVERY_CHOISES)
    discount = models.IntegerField(verbose_name='Discount', default=0)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    battery_capacity = models.CharField(verbose_name='Battery Capacity (e.g., 3.2 kWh)', max_length=20, blank=True, null=True)
    range_per_charge = models.IntegerField(verbose_name='Range per Charge (km)', null=True, blank=True)
    voltage = models.CharField(verbose_name='Voltage (e.g., 48V)', max_length=10, blank=True, null=True)

    def clean(self):
        if self.delevery_option == "paid":
            if self.shipping_cost is None or self.shipping_cost <= 0:
                raise ValidationError("Shipping cost must be provided and greater than 0 for paid delivery.")
        elif self.delevery_option == "free":
            self.shipping_cost = 0

    def __str__(self) -> str:
        return self.name.title()
    
class Cart(models.Model):
    user = models.OneToOneField(to=User, related_name="cart", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItems(models.Model):
    cart = models.ForeignKey(to=Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
    
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    order_picked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.sender} to {self.receiver}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_orders')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
