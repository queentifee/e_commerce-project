
from django.urls import path
from .views import product_list, product_detail, add_to_cart, view_cart, shopping_cart

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart,name='view_cart'),
    path('shopping_cart/', shopping_cart, name='shopping_cart'),
]
