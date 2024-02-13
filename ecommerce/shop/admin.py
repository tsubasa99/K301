from django.contrib import admin
from .models import Size, Color, GeneralCategory, Category, Campaign, Product, ProductImage
from customer.models import Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['image_tag']
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    readonly_fields = ['customer', 'star_count', 'comment']
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ReviewInline]
    list_filter = ['categories']

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(GeneralCategory)
admin.site.register(Category)
admin.site.register(Campaign)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
