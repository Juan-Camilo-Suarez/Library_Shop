from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Subquery, OuterRef
from django.db.models import Count

from app.models import Author, Employee, Client, Order, Book
from app.serializers import AuthorSerializer, OrderSerializer, BookSerializer
from app.tasks import send_feedback_email_task

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
    """http://127.0.0.1:8000/api/v1/books?pk=1"""
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


@api_view()
def get_order_info(request):
    """http://127.0.0.1:8000/api/v1/orders?pk=2"""
    order_pk = request.GET.get('pk')
    key_cache = f"order-{order_pk}"
    my_client = cache.get(key_cache)
    data = {}
    if my_client is None:
        order = Order.objects.select_related().get(pk=order_pk)
        data[order.id] = {
            "employee": order.employee.name,
            "book": order.book.name,
            "client": order.client.name
        }

        cache.set(key_cache, data, CACHE_TTL)
        return Response(data)
    else:
        return Response(my_client)


@api_view()
def get_clients_by_university(request):
    """http://127.0.0.1:8000/api/v1/clients_clasification?university=1"""
    university = request.GET.get('university')
    data = {}
    clients = Client.objects.filter(university=university)
    orders_of_client_from_university = Order.objects.filter(client__in=Subquery(clients.values('id')))
    students_id = [i.id for i in orders_of_client_from_university]
    data[university] = students_id
    return Response(data)


@api_view(['GET'])
def get_most_frequently_client(request):
    """http://127.0.0.1:8000/api/v1/clients_clasification?university=1"""
    data = {}
    client_orders_count = (Client.objects.annotate(order_count=Count('orders')).
                           order_by('-order_count').values('id', 'name', 'order_count'))
    print(type(client_orders_count))
    data = client_orders_count[0]['id'] = {
        'name': client_orders_count[0]['name'],
        'total_orders': client_orders_count[0]['order_count']
    }
    return Response(data)


@api_view()
def get_author_by_books_price(request):
    """http://127.0.0.1:8000/api/v1/clients_clasification?price=4000"""
    price = request.GET.get('price')
    data = {}
    subquery = Book.objects.filter(authors__id=OuterRef('id'), price=str(price)).values('authors__id')
    authors = Author.objects.filter(id__in=Subquery(subquery))
    for a in authors:
        data[a.id] = a.name
    return Response(data)


# ModelViewSet have default implementation CRUD operations
class AuthorViewSetModel(viewsets.ModelViewSet):
    """
        A viewset for viewing and editing Author instances.
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


# ViewSet have actions to handler request based on class
class OrderViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            client_id = order.client.id
            employee_id = order.employee.id
            book_id = order.book.id
            send_feedback_email_task.delay(client_id, employee_id, book_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# APIView have http methods to handler request based on class
class BooksApiView(APIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = self.serializer_class(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
