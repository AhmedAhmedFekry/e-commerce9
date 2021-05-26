from celery import task
from django.core.mail import send_mail
from order.models import Order
from project import settings


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    # print("the order id is                 ", order_id)
    return order_id
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = (
        f"Dear {order.first_name},\n\n"
        f"You have successfully placed an order."
        f"Your order ID is {order.id}."
    )
    mail_sent = send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        ["ahmedahmedfekry11305654@gmail.com"],
    )

    return mail_sent