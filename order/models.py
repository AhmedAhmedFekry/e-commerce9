from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from product.models import Product, Variants
from datetime import datetime
from coupons.models import Coupon
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL, blank=True, null=True
    )  # relation with varinat

    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return self.product.price

    @property
    def Total_Pr(self):
        return self.quantity * self.variant.price

    @property
    def Total_Price(self):
        return self.quantity * self.product.price


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ["quantity"]


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Preaparing", "Preaparing"),
        ("OnShipping", "OnShipping"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    # total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))

    @property
    def timeday(self):
        return self.update_at.strftime("%d/%m/%Y")

    class Meta:
        ordering = ("create_at",)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "address", "phone", "city", "country"]


class OrderProduct(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Canceled", "Canceled"),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        Variants, on_delete=models.SET_NULL, blank=True, null=True
    )  # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    # amount = models.FloatField()
    # status = models.CharField(max_length=10, choices=STATUS, default="New")
    # create_at = models.DateTimeField(auto_now_add=True)
    # update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    @property
    def Total_Pr(self):
        return self.quantity * self.variant.price

    @property
    def Total_Price(self):
        return self.quantity * self.product.price

    def get_cost(self):
        return self.price * self.quantity