from urllib import request
from multiprocessing.managers import Token
from rest_framework.response import Response
from rest_framework import (generics , status)
from Users.models import CustomUser
from django.db.models import Q
from Products.serializers import (
    CategorySerializer,
    CategoryAttributeOptionSerializer,
    CategoryAttributeSerializer,
    ContactInfoSerializer,
    LocationSerializer,
    CategoryTreeSerializer,
    ProductReadSerializer,
    ProductAttributeValueSerializer,
    ProductImageSerializer,
    ProductWriteSerializer
)
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
from rest_framework.permissions import (IsAuthenticated,AllowAny)

class ProductsListCreateView(generics.ListCreateAPIView):
    # throttle_classes =[AnonRateThrottle,UserRateThrottle]
    queryset = Product.objects.all()
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer
        return ProductReadSerializer

    def get(self,request,*args, **kwargs):
        response = super().get(request,*args,**kwargs)
        return Response(
            {
                "message": "Products Fetched successfully! .",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def post(self,request,*args, **kwargs):
        response = super().post(request,*args,**kwargs)
        return Response(
            {
                "message": "Product Created successfully! .",
                "data": response.data
            },
            status=status.HTTP_201_CREATED
        )
           
class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductReadSerializer
        return ProductWriteSerializer
    
    def get_queryset(self):
        
        if self.request.method == "GET":
            return Product.objects.all()

        return Product.objects.filter(owner=self.request.user) 
    
    def get(self,request,*args, **kwargs):
        response = super().get(request,*args,**kwargs)
        return Response(
            {
                "message": "Product Fetched successfully! .",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )
    

    def put(self,request,*args, **kwargs):
        response = super().put(request,*args,**kwargs)
        return Response(
            {
                "message": "Product Updated successfully! .",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )

    def patch(self,request,*args, **kwargs):
        response = super().patch(request,*args,**kwargs)
        return Response(
            {
                "message": "Product Updated successfully! .",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self,request,*args, **kwargs):
        response = super().delete(request,*args,**kwargs)
        return Response(
            {
                "message": "Product Deleted successfully! .",
                "data": response.data
            },
            status=status.HTTP_204_NO_CONTENT
        )

class MyProductsView(generics.ListAPIView):
    serializer_class = ProductReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list = Product.objects.all().filter(owner=self.request.user)
        return list    

class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductReadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get("q")

        queryset = Product.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Products fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class ProductFilterView(generics.ListAPIView):
    serializer_class = ProductReadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "message": "Products fetched successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)

class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "message": "Category fetched successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategoryTreeSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "message": "Categories fetched successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)
    

class CategoryAttributesView(generics.ListAPIView):
    serializer_class = CategoryAttributeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return CategoryAttribute.objects.filter(category_id=category_id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "message": "Category attributes fetched successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)
