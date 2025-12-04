from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Shipping

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Shipping)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'quantity', 'unit_price', 'total_price')
    can_delete = False  # Optional: prevent admin deletion of items

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number',)
    inlines = [OrderItemInline]  # 👈 This displays order items on detail page
    
    readonly_fields = ('order_number', 'created_at', 'updated_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


