from django.urls import path
from cart import views as cview

urlpatterns = [
    path("basket_add/", cview.basket_add, name="basket_add"),
    path("basket_add_detail/", cview.basket_add_detail, name="basket_add_detail"),
    path("basket_delete", cview.basket_delete, name="basket_delete"),
    path("basket_update/", cview.basket_update, name="basket_update"),
]
