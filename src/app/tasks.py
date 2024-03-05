from django.core.mail import send_mail
from celery import shared_task

from app.models import Client, Employee, Book
from project import settings


@shared_task()
def send_feedback_email_task(client_id, employee_id, book_id):
    client = Client.objects.get(pk=client_id)
    employee = Employee.objects.get(pk=employee_id)
    book = Book.objects.get(pk=book_id)

    send_mail(
        "Your Order",
        f"\t Good Moorning {client.name} \t your support employee is: {employee.name}\t Your book: {book.name} \t Thank you!",
        settings.EMAIL_HOST_USER,
        [client.email],
        fail_silently=False,
    )
