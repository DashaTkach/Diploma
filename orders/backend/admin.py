from django.contrib import admin

from .models import *


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'user_id')
    list_display_links = ('id', 'name', 'url')
    search_fields = ('name', 'user_id',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_id')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'category_id',)


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'price_rrc', 'quantity', 'product_id', 'shop_id')
    list_display_links = ('id', 'quantity', 'price', 'price_rrc')
    search_fields = ('name', 'product_id', 'shop_id',)


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'value', 'parameter_id', 'product_info_id')
    list_display_links = ('id', 'value')
    search_fields = ('name', 'parameter_id', 'product_info_id',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone', 'user_id')
    list_display_links = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
    search_fields = ('user_id',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'dt', 'contact_id', 'user_id', 'state')
    list_display_links = ('id', 'dt', 'state')
    search_fields = ('contact_id', 'user_id',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'order_id', 'product_info_id', 'shop_id')
    list_display_links = ('id', 'quantity')
    search_fields = ('order_id', 'product_info_id', 'shop_id',)


admin.site.register(Shop, ShopAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
