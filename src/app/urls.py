from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from app import views

router = routers.SimpleRouter()

router.register('author', views.AuthorViewSetModel)

urlpatterns = [
    path('books', views.get_book_by_authors, name='get book by author pk'),
    path('orders', views.get_orders_by_client, name='get orders_by_client'),
    path('order', views.get_order_info, name='get order'),
    path('', include(router.urls)),
]
