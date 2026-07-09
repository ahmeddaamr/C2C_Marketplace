from django.urls import path, include
from .views import views

urlpatterns = [
    
    #Products
    path("",views.ProductsListCreateView.as_view(),name="products"),
    path("<int:pk>/",views.ProductRetrieveUpdateDeleteView.as_view(),name="product-detail"),
    path("myProducts/", views.MyProductsView.as_view(), name="my-products" ),
    path("search/",views.ProductSearchView.as_view(),name="product-search"),
    path("filter/",views.ProductFilterView.as_view(),name="product-filter"),
    
    # Categories
    path("category/<int:pk>",views.CategoryRetrieveView.as_view(),name="categories"),
    path("categories/",views.CategoryListView.as_view(),name="categories"),
    path("category/<int:pk>/attributes/",views.CategoryAttributesView.as_view(),name="category-attributes"),
]