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
    path('order_create', views.OrderViewSet.as_view({'post': 'create'})),
    path('clients_clasification', views.get_clients_by_university, name='get clients id by university'),
    path('books_list', views.BooksApiView.as_view()),
    path('best_client', views.get_most_frequently_client, name='best client'),
    path('author_book_price', views.get_author_by_books_price, name='author_book_price'),
    path('', include(router.urls)),
]
