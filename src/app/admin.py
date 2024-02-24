from django.contrib import admin

from app.models import Client, Employee, Author, Book, Order

# Register your models here.
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Order)