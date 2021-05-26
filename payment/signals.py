from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED  # completed
from paypal.standard.ipn.signals import valid_ipn_received
from order.models import Order


def payment_notification(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        Order = get_object_or_404(Order, id=ipn_obj.invoice)

        Order.update(paid=True)
        Order.save()


valid_ipn_received.connect(payment_notification)