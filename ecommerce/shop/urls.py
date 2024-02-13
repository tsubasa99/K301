from django.urls import path
from .import views

app_name='shop'
urlpatterns=[
    path('',views.home,name='home'),
    path('products', views.product_list,name='product-list'),
    path('products/<int:pk>/', views.product_detail,name='product-detail'),
    path('review/<int:pk>/', views.review, name='review'),


]
