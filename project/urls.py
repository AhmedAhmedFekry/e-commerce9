"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from home import views
from product import views as pviews
from order import views as OrderViews
from user import views as UserViews
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path("selectlanguage", views.selectlanguage, name="selectlanguage"),
    path("selectcurrency", views.selectcurrency, name="selectcurrency"),
    # path('savelangcur', views.savelangcur, name='savelangcur'),
    path("i18n/", include("django.conf.urls.i18n")),
    # path("admin/order/<int:id>/pdf_view/", OrderViews.pdforder, name="pdf_view"),
]
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("currencies/", include("currencies.urls")),
    path("", include("home.urls")),
    path("accounts/", include("allauth.urls")),
    # path("social-auth/", include("social_django.urls", namespace="social")),
    # path("ajaxs/prices/", pviews.ajaxprice, name="plist"),
    path("product/", include("product.urls"), name="product"),
    path("order/", include("order.urls"), name="order"),
    path("cart/", include("cart.urls"), name="cart"),
    path("user/", include("user.urls"), name="user"),
    path("coupons/", include("coupons.urls"), name="coupons"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("shopcart/", OrderViews.shopcart, name="shopcart"),
    path("login/", UserViews.login_form, name="login"),
    path("logout/", UserViews.logout_func, name="logout"),
    path("signup/", UserViews.signup_form, name="signup"),
    path("search/", views.search, name="search"),
    path("search_auto/", views.search_auto, name="search_auto"),
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("payment/", include("payment.urls")),
    prefix_default_language=True,
)
if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)