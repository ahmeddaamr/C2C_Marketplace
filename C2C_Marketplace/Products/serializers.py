from rest_framework import serializers
from Products.models import (
    Product,
    Category,
    CategoryAttribute,
    CategoryAttributeOption,
    ContactInfo,
    Location,
    ProductAttributeValue,
    ProductImage
    )
# from Users.serializers import Token

# 1) SIMPLE SERIALIZERS

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'path',
            'level',
            'icon',
            'is_active',
            'parent'
        ]

class CategoryAttributeOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryAttributeOption
        fields = [
            'id',
            'value'
        ]

class CategoryAttributeSerializer(serializers.ModelSerializer):

    options = CategoryAttributeOptionSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = CategoryAttribute
        fields = [
            'id',
            'name',
            'data_type',
            'required',
            'filterable',
            'searchable',
            'options'
        ]

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'

class ContactInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactInfo
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'image',
            'order',
            'is_primary'
        ]

# 2) READ SERIALIZERS

class ProductAttributeValueSerializer(
    serializers.ModelSerializer
):

    attribute_name = serializers.CharField(
        source='attribute.name',
        read_only=True
    )

    class Meta:
        model = ProductAttributeValue
        fields = [
            'id',
            'attribute',
            'attribute_name',
            'value'
        ]

class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    contactInfo = ContactInfoSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    # owner = Token()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'payment_option',
            'price',
            'is_negotiable',
            'listing_type',
            'is_active',
            'created_at',
            'owner',
            'category',
            'location',
            'contactInfo',
            'attribute_values',
            'images',
        ]


class ProductWriteSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product

        fields = [
            'title',
            'description',
            'payment_option',
            'price',
            'is_negotiable',
            'listing_type',
            'category',
            'location',
            'contactInfo',
            'images'
            # 'owner',
        ]

    def create(self, validated_data):

        print (validated_data)

        images = validated_data.pop("images", [])

        product = Product.objects.create(**validated_data)

        for index, image in enumerate(images):

            ProductImage.objects.create(
                product=product,
                image=image,
                order=index,
                is_primary=(index == 0)
            )

        return product

class CategoryTreeSerializer( serializers.ModelSerializer):

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'children'
        ]

    def get_children(self, obj):
        return CategoryTreeSerializer( obj.children.all(),many=True).data