from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

from app.models import Author, Client

# Cache time to live is 30 minutes.
CACHE_TTL = 60 * 30


@api_view()
def get_book_by_authors(request):
    """http://127.0.0.1:8000/api/weather?pk=1"""
    author_pk = request.GET.get('pk')
    my_value = cache.get(author_pk)
    data = {}
    if my_value is None:
        author = Author.objects.prefetch_related('books').get(pk=author_pk)
        for a in author.books.all():
            data[a.id] = a.name

        cache.set(author_pk, data, CACHE_TTL)
        return Response(data)
    else:
        return Response(my_value)


@api_view()
def get_orders_by_client(request):
    """http://127.0.0.1:8000/api/weather?pk=1"""
    client_pk = request.GET.get('pk')
    key_cache = f"orders-{client_pk}"
    my_client = cache.get(key_cache)
    data = {}
    if my_client is None:
        client = Client.objects.prefetch_related('orders').get(pk=client_pk)
        for cli in client.orders.all():
            data[cli.id] = {
                "employee": cli.employee.name,
                "book": cli.book.name
            }

        cache.set(key_cache, data, CACHE_TTL)
        return Response(data)
    else:
        return Response(my_client)
