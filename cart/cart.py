from decimal import Decimal
from django.conf import settings
from product.models import Product, Variants
from coupons.models import Coupon


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product, quantity=1, variantid=None, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        if variantid != None:
            print("Add a product to the cart or update its quantity.", str(product.id))
            variant = Variants.objects.get(id=variantid)
            # print("the price in the variant is ", variant.price)
            print("the variant isvvvvvvvvvvvvvvvvvv  ", variant)
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {
                    "quantity": 0,
                    "variantid": variantid,
                    "price": str(variant.price),
                }
            if override_quantity:
                self.cart[product_id]["quantity"] = quantity
            else:
                self.cart[product_id]["quantity"] += quantity
                print(
                    "the quantity in the ccart is ", self.cart[product_id]["quantity"]
                )
        else:
            # print("Add a product to the cart or update its quantity.", str(product.id))
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {
                    "quantity": 0,
                    "variantid": None,
                    "price": str(product.price),
                }
            if override_quantity:
                self.cart[product_id]["quantity"] = quantity
            else:
                self.cart[product_id]["quantity"] += quantity
                print(
                    "the quantity in the ccart is ", self.cart[product_id]["quantity"]
                )
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            if product.variant != None:
                # print(
                #     "ppppppppppppppppppppppppppp",
                #     self.cart[str(product.id)]["variantid"],
                # )
                # vid = self.cart[str(product.id)]["variantid"]
                # variant = Variants.objects.get(id=vid)
                # print("the variant isvvvvvvvvvvvvvvvvvv  ffffffffffff ", variant)
                # print("the variant isvvvvvvvvvvvvvvvvvv  ffffffffffff ", variant.price)
                cart[str(product.id)]["product"] = product
                # cart[str(product.id)]["variant"] = variant
                # cart[str(product.id)]["variant"] = product
            else:
                cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]

            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """

        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            print(
                " delete from cart class is successedddddddddddddddddddddddddddddddddddddddddddddddddddddd "
            )
            self.save()

    def clear(self):
        # remove cart from session
        # del self.session["coupon_id"]
        del self.session[settings.CART_SESSION_ID]
        del self.session["coupon_id"]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
