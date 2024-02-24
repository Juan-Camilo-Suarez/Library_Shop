from django.db import models


# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=12)
    university = models.CharField(max_length=200, null=True, blank=True)


class Employee(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=12)
    salary = models.CharField(max_length=6, null=False, blank=False)


class Author(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    university = models.CharField(max_length=200, null=True, blank=True)
    age = models.CharField(max_length=2)


class Book(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.CharField(max_length=5, null=False, blank=False)
    authors = models.ManyToManyField(Author, related_name='books')


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order')
