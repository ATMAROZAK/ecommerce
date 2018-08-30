from django.contrib import admin
from .models import Category, Subcategory, Brand, Product

#Модель бренда
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

# Модель подкатегории
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'subcategory', 'slug', 'price', 'stock', 'available']
    list_filter = ['available', 'brand', 'category', 'subcategory']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
