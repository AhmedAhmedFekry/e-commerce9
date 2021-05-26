from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from order.models import Order, ShopCart

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def payment_done(request):
    current_user = request.user
    ShopCart.objects.filter(user_id=current_user.id).delete()
    return render(request, "payment/done.html")


@csrf_exempt
def payment_canceled(request):
    return render(request, "payment/canceled.html")


def payment_process(request):

    order_id = request.session.get("order_id")
    orders = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "%.2f" % orders.total,
        "item_name": "Order {}".format(orders.id),
        "invoice": str(orders.id),
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment:done")),
        "cancel_return": "http://{}{}".format(host, reverse("payment:canceled")),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "order": orders,
        "form": form,
    }
    return render(request, "payment/process.html", context)
