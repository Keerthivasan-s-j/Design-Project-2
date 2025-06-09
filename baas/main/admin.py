from django.contrib import admin
from .models import UserProfile, Product, Cart, CartItems, Notification, Order, OrderItem

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'category', 'delevery_option',
        'battery_capacity', 'range_per_charge', 'voltage',
        'discount', 'shipping_cost'
    )
    list_filter = ('category', 'delevery_option')
    search_fields = ('name', 'details', 'battery_capacity', 'voltage')

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'image', 'details')
        }),
        ('EV Specifications', {
            'fields': ('battery_capacity', 'range_per_charge', 'voltage')
        }),
        ('Pricing & Delivery', {
            'fields': ('price', 'discount', 'category', 'delevery_option', 'shipping_cost')
        }),
    )

@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    search_fields = ('product__prod_name',)

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'is_read', 'order_picked', 'created_at']
    list_filter = ['is_read', 'order_picked']
    search_fields = ['sender__username', 'receiver__username']

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'product', 'quantity', 'status', 'delivery_agent', 'created_at']
#     list_filter = ['status']
#     search_fields = ['user__username', 'product__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total_amount']  # remove invalid fields
    search_fields = ['user__username', 'city', 'state']
    list_filter = ['created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']