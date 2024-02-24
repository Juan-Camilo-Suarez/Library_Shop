from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('books', views.get_book_by_authors, name='get book by author pk'),

]
