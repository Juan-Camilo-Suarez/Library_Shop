from rest_framework import serializers

from app.models import Order, Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'email', 'university', 'age']

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['client', 'employee', 'book']

# class BookSerializer(serializers.ModelSerializer):
#     authors =
#     class Meta:
#         model = Book
#         fields = ['name', 'price', 'authors']
