from django.contrib import admin
from .models import Product, Variation
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['id', 'product_name', 'slug', 'price', 'stock', 'is_available', 'category']
    list_display_links = ['id', 'product_name', 'slug', 'price', 'stock', 'is_available', 'category']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'variation_category', 'variation_value', 'is_active']
    list_editable = ('is_active',)
    list_filter = ['product', 'variation_category', 'variation_value']
