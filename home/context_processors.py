from order.models import ShopCart

# import requests
from django.shortcuts import render

from django.http import JsonResponse
from product.models import Category
from cart.cart import Cart


def totalprice(request):
    basket = Cart(request)
    basketqty = basket.__len__()
    baskettotal = basket.get_total_price_after_discount()
    return {"tot": baskettotal, "countt": basketqty}
