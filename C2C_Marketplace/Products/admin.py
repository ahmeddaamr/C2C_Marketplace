from django.contrib import admin
from Products.models import (
    Category,
    CategoryAttribute,
    CategoryAttributeOption,
    Location,
    ProductImage ,
    Product,
    ProductAttributeValue,
    ContactInfo
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "price",
        "category",
        "location",
        "is_active",
        "created_at",
        "listing_type",
        "payment_option",
        "owner"
    )

    list_filter = (
        "category",
        "location",
        "is_active",
        "payment_option",
        "listing_type",
        "owner",
    )

    search_fields = (
        "title",
        "description"
    )

    readonly_fields = (
        "created_at",   
    )

    inlines = [
        ProductImageInline,
        ProductAttributeValueInline
    ]

class CategoryAttributeOptionInline(admin.TabularInline):
    model = CategoryAttributeOption
    extra = 1

@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "data_type",
        "required",
        "filterable"
    )

    list_filter = (
        "category",
        "data_type"
    )

    search_fields = (
        "name",
    )

    inlines = [
        CategoryAttributeOptionInline
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "id",
        "parent",
        "level",
        "path",
        "is_active"
    )

    list_filter = (
        "level",
        "is_active"
    )

    search_fields = (
        "name",
        "slug"
    )

    readonly_fields = (
        "path",
        "level",
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone_number",
        "contact_method"
    )

    search_fields = (
        "name",
        "phone_number"
    )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "city",
        "state",
        "country"
    )

    search_fields = (
        "city",
        "state",
        "country"
    )
    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "order",
        "is_primary"
    )

    list_filter = (
        "is_primary",
    )


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "attribute",
        "value"
    )

    list_filter = (
        "attribute",
    )

    search_fields = (
        "value",
    )
    

# admin.site.register(Category)
# admin.site.register(CategoryAttribute)
# admin.site.register(CategoryAttributeOption)
# admin.site.register(ContactInfo)
# admin.site.register(Location)
# admin.site.register(Product)
# admin.site.register(ProductAttributeValue)
# admin.site.register(ProductImage)
# # admin.site.register(PaymentOption)