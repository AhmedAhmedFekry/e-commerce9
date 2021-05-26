from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product, Category
from home.models import Setting, ContactForm, ContactMessage, Offer, FAQ
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import translation
from project import settings
from order.models import ShopCart, ShopCartForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from . import context_processors
from django.core.paginator import Paginator
from django.db.models import Max, Min
from cart.cart import Cart
from home.forms import SearchForm
import json
from django.db.models import Q


# Create your views here.
def home(request):
    current_user = request.user  # Access User Session information
    if not request.session.has_key("currency"):
        request.session["currency"] = settings.DEFAULT_CURRENCY
    offers = Offer.objects.all()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    products = Product.objects.filter(startpage=True, status=True).order_by("?")
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    count = ShopCart.objects.filter(user_id=current_user.id).count()
    total = 0
    tot = context_processors.totalprice(request)
    data = {
        "products": products,
        "setting": setting,
        "category": category,
        "offers": offers,
        "count": count,
        "total": tot["tot"],
    }
    return render(request, "pages/home.html", data)


def aboutus(request):

    category = Category.objects.all()
    # defaultlang = settings.LANGUAGE_CODE[0:2]
    # currentlang = request.LANGUAGE_CODE[0:2]
    setting = Setting.objects.get(pk=1)
    # if defaultlang != currentlang:
    #     setting = SettingLang.objects.get(lang=currentlang)

    context = {
        "setting": setting,
        "category": category,
    }
    return render(request, "pages/about.html", context)


def contactus(request):
    category = Category.objects.all()
    # currentlang = request.LANGUAGE_CODE[0:2]
    # category = categoryTree(0,'',currentlang)
    if request.method == "POST":  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data["name"]  # get form input data
            data.email = form.cleaned_data["email"]
            data.subject = form.cleaned_data["subject"]
            data.message = form.cleaned_data["message"]
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()  # save data to table
            messages.success(
                request, "Your message has ben sent. Thank you for your message."
            )
            return HttpResponseRedirect("/Cantact-us")

    # defaultlang = settings.LANGUAGE_CODE[0:2]
    # currentlang = request.LANGUAGE_CODE[0:2]
    setting = Setting.objects.get(pk=1)
    # if defaultlang != currentlang:
    #     setting = SettingLang.objects.get(lang=currentlang)

    form = ContactForm
    context = {"setting": setting, "form": form, "category": category}
    return render(request, "pages/contactus.html", context)


def category_products(request, id, slug):
    category = Category.objects.all()
    categ = Category.objects.get(pk=id)
    print("category product done")
    products = Product.products.filter(category__id=id)
    maxb = products.aggregate(Max("price"))
    minb = products.aggregate(Min("price"))
    print("the max in category page is ", maxb)
    print("the min in category page is ", minb)
    print(maxb["price__max"])
    paginator = Paginator(products, 9)

    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    print(type(page_number))
    if page_number == None:
        page_number = "1"

    page_number = int(page_number)
    context = {
        "products": products,
        "categ": categ,
        "category": category,
        "number": page_number,
        "maxb": maxb,
        "minb": minb,
    }
    return render(request, "pages/category_products.html", context)


def faq(request):
    category = Category.objects.all()
    # defaultlang = settings.LANGUAGE_CODE[0:2]
    # currentlang = request.LANGUAGE_CODE[0:2]

    # if defaultlang == currentlang:
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    # else:
    #     faq = FAQ.objects.filter(
    #         status="True", lang=currentlang).order_by("ordernumber")

    context = {"faq": faq, "category": category}
    return render(request, "pages/faq.html", context)


def selectlanguage(request):
    if request.method == "POST":  # check post
        cur_language = translation.get_language()
        lasturl = request.META.get("HTTP_REFERER")
        lang = request.POST["language"]
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        # return HttpResponse(lang)
        return HttpResponseRedirect("/" + lang)


def selectcurrency(request):
    lasturl = request.META.get("HTTP_REFERER")
    if request.method == "POST":  # check post
        request.session["currency"] = request.POST["currency"]
    return HttpResponseRedirect(lasturl)


@login_required(login_url="/login")
def addtoshopcartajax(request):
    data = {"ahmed": "kks"}
    d = request.GET.get("prosuctid")

    print("hhhhhwwww ffffffffffffffffffff                ", request.POST)
    print(d)

    url = request.META.get("HTTP_REFERER")  # get last url
    current_user = request.user  # Access User Session information

    product = Product.objects.get(pk=d)

    if product.variant != "None":
        variantid = request.POST.get("variantid")  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(
            variant_id=variantid, user_id=current_user.id
        )  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(
            product_id=d, user_id=current_user.id
        )  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == "POST":  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                if product.variant == "None":
                    data = ShopCart.objects.get(product_id=d, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(
                        product_id=d, variant_id=variantid, user_id=current_user.id
                    )
                data.quantity += form.cleaned_data["quantity"]
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = d
                data.variant_id = variantid
                data.quantity = form.cleaned_data["quantity"]
                data.save()
        messages.success(request, "Product added to Shopcart ")
        count = ShopCart.objects.filter(user_id=current_user.id).count()
        shopcart = ShopCart.objects.filter(user_id=current_user.id)

        total = 0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
        print("the shop cart product is", shopcart)
        print(total, "tttttttttttttttttttttttttttttttttttttt")

        context = {"shopcart": shopcart}
        data["html_ShopCart"] = render_to_string(
            "ajax_pages/shopping-cart-list.html", context, request=request
        )
        data["count"] = count
        data["total"] = total

        return JsonResponse(data)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            print(" Update  shopcart")
            data = ShopCart.objects.get(product_id=d, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            print("Inser to Shopcart")
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = d
            data.quantity = 1
            data.variant_id = None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        count = ShopCart.objects.filter(user_id=current_user.id).count()

    count = ShopCart.objects.filter(user_id=current_user.id).count()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    print(total, "tttttttttttttttttttttttttttttttttttttt")
    print("the shop cart product is", shopcart)
    context = {"shopcart": shopcart, "request": request}
    html_ShopCart = render_to_string(
        "ajax_pages/shopping-cart-list.html", context, request=request
    )
    data = {"count": count, "total": total, "html_ShopCart": html_ShopCart}
    return JsonResponse(data)


def shoplist(request):
    data = dict()
    basket = Cart(request)
    print("shoplist functions done")

    context = {"cart": basket, "request": request}
    data["html_ShopCart"] = render_to_string(
        "includes/shopping-cart-list.html", context, request=request
    )
    print("shoplist functions done afrerfffffffffffffffffffffffffff")
    return JsonResponse(data)


def deleteshoplist(request):
    basket = Cart(request)
    data = dict()
    print("lllllllllllllllllllllllll")
    print(request.GET.get("productiddelete"))
    id = request.GET.get("productiddelete")
    basket.delete(product=id)

    basketqty = basket.__len__()
    baskettotal = basket.get_total_price()
    print("iiiiiiiiiiiiii", baskettotal)
    tot = render_to_string("includes/total.html", {"tot": baskettotal}, request=request)
    response = JsonResponse({"tot": tot, "qty": basketqty})

    return response


def search(request):
    if request.method == "POST":  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]  # get form input data
            catid = form.cleaned_data["catid"]
            if catid == 0:
                products = Product.objects.filter(
                    Q(title__icontains=query)
                    | Q(title_ar__icontains=query)
                    | Q(title_en__icontains=query)
                )  # SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(
                    Q(title__icontains=query)
                    | Q(title_ar__icontains=query)
                    | Q(title_en__icontains=query)
                )

            category = Category.objects.all()
            context = {"products": products, "query": query, "category": category}
            return render(request, "pages/search_products.html", context)

    return HttpResponseRedirect("/")


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get("term", "")
        products = Product.objects.filter(
            Q(title__icontains=q) | Q(title_ar__icontains=q) | Q(title_en__icontains=q)
        )

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title + " > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = "fail"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)