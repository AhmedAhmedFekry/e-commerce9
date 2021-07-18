import weasyprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from order.models import ShopCart, ShopCartForm, Order, OrderForm, OrderProduct
from product.models import Category, Product, Variants
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.views import View
from django.contrib.auth.models import User
from user.models import UserProfile
from django.core.mail import EmailMessage
from project import settings
from django.utils.crypto import get_random_string
from home.context_processors import totalprice
from cart.cart import Cart
from django.core import serializers
import json
from order.tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from coupons.forms import CouponApplyForm
from weasyprint import HTML
import tempfile


from django.contrib.admin.views.decorators import staff_member_required


def shopcart(request):
    basket = Cart(request)
    print("bbbbbbbbbbbbbbbb", basket.cart)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    # return HttpResponse(str(total))
    count = ShopCart.objects.filter(user_id=current_user.id).count()
    coupon_apply_form = CouponApplyForm()
    context = {
        "cart": basket,
        "category": category,
        "total": total,
        "count": count,
        "coupon_apply_form": coupon_apply_form,
    }
    return render(request, "pages/shopcart_products.html", context)


def order_created(request):
    category = Category.objects.all()

    cart = Cart(request)
    for item in cart:
        print('ff', item["product"])
    data = json.loads(request.body)
    print('the request ', data )
    print('the request ', data['form'] )
    print('the cart is ', cart )
    f=data['form']
    user=request.user
    order=Order.objects.create(user=user,first_name=f['first_name'],last_name=f['last_name'],address=f['address'],phone=f['phone'],city=f['city'],country=f['country'])
    order.save()
    print('order is created done 2 ')
    for item in cart:
            OrderProduct.objects.create(
                    order=order,
                    product=item["product"],
                    variant=None,
                    price=item["price"],
                    quantity=item["quantity"],
                )
    print('order is created done 1 ')
    messages.success(request, "Payment was successful")
    cart.clear()
    return redirect('home')


    # if request.method == "POST":
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         order = form.save(commit=False)
    #         if cart.coupon:
    #             order.coupon = cart.coupon
    #             order.discount = cart.coupon.discount
    #         order.save()
    #         for item in cart:
    #             OrderProduct.objects.create(
    #                 order=order,
    #                 product=item["product"],
    #                 variant=None,
    #                 price=item["price"],
    #                 quantity=item["quantity"],
    #             )
    #         # clear the cart
    #         cart.clear()
    #         # launch asynchronous task
    #         # order_created.delay(order.id)

    #         return render(
    #             request,
    #             "pages/Order_Completed.html",
    #             {"category": category, "order": order},
    #         )
    # else:
    #     form = OrderForm()
    # return render(
    #     request,
    #     "pages/Order_Form.html",
    #     {
    #         "cart": cart,
    #         "form": form,
    #         "category": category,
    #     },
    # )


def orderproductpaypal(request):
    return redirect(reverse("payment:process"))


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(
#         BytesIO(html.encode("UTF-8")),
#         result,
#         encoding="UTF-8",
#     )
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type="application/pdf")
#     return None


# data = {
#     "company": "Dennnis Ivanov Company",
#     "address": "123 Street name",
#     "city": "Vancouver",
#     "state": "WA",
#     "zipcode": "98663",
#     "phone": "555-555-2345",
#     "email": "youremail@dennisivy.com",
#     "website": "dennisivy.com",
# }

# # Opens up page as PDF


# def pdforder(request, id):
#     order = Order.objects.get(id=id)
#     print(" order ", order.first_name)
#     orderitems = OrderProduct.objects.filter(order_id=id)
#     print(" lllllllllll ", orderitems)
#     total = 0
#     for rs in orderitems:
#         total += rs.product.price * rs.quantity
#     pdf = render_to_pdf(
#         "admin/orders/order/pdf_template.html",
#         {"order": order, "orderitems": orderitems, "total": total, "id": id},
#     )
#     return HttpResponse(pdf, content_type="application/pdf")


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("admin/orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + "/css/pdf.css")]
    )
    return response

















def order_create(request):
    print('lllllllllllllllllllllllllllllllllllllll')
    category = Category.objects.all()
    cart = Cart(request)
    user=request.user
    print('the cart is ', cart )
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user=user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderProduct.objects.create(
                    order=order,
                    product=item["product"],
                    variant=None,
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)

            return render(
                request,
                "pages/Order_Completed.html",
                {"category": category, "order": order},
            )
    else:
        form = OrderForm()
    return render(
        request,
        "pages/Order_Form.html",
        {
            "cart": cart,
            "form": form,
            "category": category,
        },
    )

