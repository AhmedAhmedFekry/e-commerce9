from django.shortcuts import get_object_or_404, render
from cart.cart import Cart
from django.http import JsonResponse
from django.template.loader import render_to_string
from product.models import Product

# Create your views here.
def basket_add(request):
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    basket = Cart(request)
    if request.POST.get("action") == "post":

        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, quantity=1, variantid=None, override_quantity=False)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price_after_discount()
        print("iiiiiiiiiiiiii", baskettotal)
        tot = render_to_string(
            "includes/total.html", {"tot": baskettotal}, request=request
        )
        response = JsonResponse({"tot": tot, "qty": basketqty})
        return response


def basket_add_detail(request):
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    basket = Cart(request)

    if request.POST.get("action") == "post":
        variantid = None

        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        productvariant = request.POST.get("productvariant")
        print("the variant id is  ", productvariant)
        product = get_object_or_404(Product, id=product_id)
        basket.add(
            product=product,
            quantity=product_qty,
            variantid=productvariant,
            override_quantity=False,
        )

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price_after_discount()
        print("iiiiiiiiiiiiii", baskettotal)
        tot = render_to_string(
            "includes/total.html", {"tot": baskettotal}, request=request
        )
        response = JsonResponse({"tot": tot, "qty": basketqty})
        return response


def basket_update(request):
    basket = Cart(request)
    if request.POST.get("action") == "post":
        print("update asket tttttttttttt")
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        print("first", basket.cart)
        produc = Product.objects.get(pk=product_id)
        basket.add(
            product=produc,
            quantity=product_qty,
            variantid=None,
            override_quantity=True,
        )

        subtotalOfProduct = basket.cart[str(product_id)]["quantity"] * float(
            basket.cart[str(product_id)]["price"]
        )
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price_after_discount()
        print("iiiiiiiiiiiiii", baskettotal)
        tot = render_to_string(
            "includes/total.html", {"tot": baskettotal}, request=request
        )
        baskettotal1 = basket.get_discount()
        tot1 = render_to_string(
            "includes/total.html", {"tot": baskettotal1}, request=request
        )
        baskettotal2 = basket.get_total_price()
        tot2 = render_to_string(
            "includes/total.html", {"tot": baskettotal2}, request=request
        )
        tot_product = render_to_string(
            "includes/total_price_of_product.html",
            {"total_price": subtotalOfProduct},
            request=request,
        )
        response = JsonResponse(
            {
                "tot": tot,
                "tot1": tot1,
                "tot2": tot2,
                "total_price": tot_product,
                "qty": basketqty,
                "subtotal": baskettotal,
                "subtotalOfProduct": subtotalOfProduct,
            }
        )
        return response


def basket_delete(request):
    basket = Cart(request)
    print("from basketttttttttttttttttttttttttttttttttttttt")
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price_after_discount()
        tot = render_to_string(
            "includes/total.html", {"tot": baskettotal}, request=request
        )
        print("the total is of basket ", baskettotal)
        baskettotal1 = basket.get_discount()
        tot = render_to_string(
            "includes/total.html", {"tot": baskettotal}, request=request
        )
        tot1 = render_to_string(
            "includes/total.html", {"tot": baskettotal1}, request=request
        )
        baskettotal2 = basket.get_total_price()
        tot2 = render_to_string(
            "includes/total.html", {"tot": baskettotal2}, request=request
        )
        response = JsonResponse(
            {
                "tot": tot,
                "tot1": tot1,
                "tot2": tot2,
                "qty": basketqty,
                "subtotal": baskettotal,
                "tot": tot,
            }
        )
        return response