from django.urls import path
from home import views
from product import views as pviews
from cart import views as cview

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us", views.aboutus, name="aboutus"),
    path("Cantact-us", views.contactus, name="cantactus"),
    path("faq/", views.faq, name="faq"),
    path(
        "category/<int:id>/<str:slug>",
        views.category_products,
        name="category_products",
    ),
    # path('pricetest', pviews.price, name='price'),
    path("like", pviews.favorite, name="like"),
    path("compare", pviews.product_compare, name="compare"),
    path("ajaxcolor/", pviews.ajaxcolor, name="ajaxcolor"),
    path("shoplist/", views.shoplist, name="shoplist"),
    path("deleteshoplist/", views.deleteshoplist, name="deleteshoplist"),
    path("pricetest", pviews.price, name="price"),
    path("category/<int:id>/ajax/prices", pviews.ajaxprice, name="plist"),
    path("basket_delete", cview.basket_delete, name="basket_delete"),
    path("basket_update/", cview.basket_update, name="basket_update"),
]
