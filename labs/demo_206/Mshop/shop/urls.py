"""
Shop URL config - same routes as demo_205 Laravel web.php.
/products, /products/create, /products/manage, /products/<id>/edit, /products/<id>, PUT/DELETE/POST buy
/transactions, /transactions/<id>, /transactions/<user_id>/user
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='index'),
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/manage/', views.product_manage, name='product_manage'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/', views.product_show, name='product_show'),
    path('products/<int:product_id>/update/', views.product_update, name='product_update'),
    path('products/<int:product_id>/delete/', views.product_destroy, name='product_destroy'),
    path('products/<int:product_id>/buy/', views.product_buy, name='product_buy'),
    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:transaction_id>/', views.transaction_show, name='transaction_show'),
    path('transactions/<int:user_id>/user/', views.transaction_list_user, name='transaction_list_user'),
]
