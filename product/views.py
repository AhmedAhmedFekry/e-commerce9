from django.shortcuts import render
from product.models import (
    Product,
    Category,
    Images,
    CommentForm,
    Comment,
    Variants,
    Compare,
    Like,
)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Max, Min
from order.models import ShopCart

# Create your views here.
def product_detail(request, id, slug):
    query = request.GET.get("q")
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    catda = Category.objects.get(pk=product.category_id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status="True")

    context = {
        "product": product,
        "category": category,
        "catda": catda,
        "images": images,
        "comments": comments,
    }
    if product.variant != "None":  # Product have variants
        if request.method == "POST":  # if we select color
            variant_id = request.POST.get("variantid")
            variant = Variants.objects.get(
                id=variant_id
            )  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw(
                "SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id",
                [id],
            )
            query += (
                variant.title
                + " Size:"
                + str(variant.size)
                + " Color:"
                + str(variant.color)
            )
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw(
                "SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id",
                [id],
            )
            variant = Variants.objects.get(id=variants[0].id)
        context.update(
            {"sizes": sizes, "colors": colors, "variant": variant, "query": query}
        )

    return render(request, "pages/product_detail.html", context)


def ajaxcolor(request):
    data = {}
    if request.POST.get("action") == "post":
        size_id = request.POST.get("size")
        productid = request.POST.get("productid")
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            "size_id": size_id,
            "productid": productid,
            "colors": colors,
            "request": request,
        }
        data = {
            "rendered_table": render_to_string(
                "ajax_Pages/color_list.html", context=context
            )
        }
        return JsonResponse(data)
    return JsonResponse(data)


def addcomment(request, id):
    url = request.META.get("HTTP_REFERER")  # get last url
    # return HttpResponse(url)
    # print('add commmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
    if request.method == "POST":  # check post
        form = CommentForm(request.POST)
        print("add commmmmmmmmmmmmmmmmmmmmmmmm")
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data["subject"]
            data.comment = form.cleaned_data["comment"]
            data.rate = form.cleaned_data["rate"]
            data.ip = request.META.get("REMOTE_ADDR")
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(
                request, "Your review has ben sent. Thank you for your interest."
            )
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


@login_required(login_url="/login")  # Check login
def addlike(request):
    url = request.META.get("HTTP_REFERER")
    user = request.user
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_obj = Product.objects.get(id=product_id)

        if user in product_obj.like.all():
            product_obj.like.remove(user)

        else:
            product_obj.like.add(request.user)

        like, created = Like.objects.get_or_create(user=user, product_id=product_id)
        if not created:
            if like.value == "like":
                like.value = "unlike"
            else:
                like.value = "like"

        like.save()
    return HttpResponseRedirect(url)


@login_required(login_url="/login")  # Check login
def favorite(request):

    category = Category.objects.all()
    products_Favorite = Product.objects.filter(like=request.user)

    return render(
        request,
        "pages/Favorite.html",
        {"products_Favorite": products_Favorite, "category": category},
    )


@login_required(login_url="/login")  # Check login
def addcompare(request):
    url = request.META.get("HTTP_REFERER")
    user = request.user
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_obj = Product.objects.get(id=product_id)

        if user in product_obj.compare.all():
            product_obj.compare.remove(user)

        else:
            product_obj.compare.add(request.user)

        compare, created = Compare.objects.get_or_create(
            user=user, product_id=product_id
        )
        if not created:
            if compare.value == "yes":
                compare.value = "no"
            else:
                compare.value = "no"

        compare.save()
    return HttpResponseRedirect(url)


@login_required(login_url="/login")  # Check login
def product_compare(request):
    products_compare = Product.objects.filter(compare=request.user)

    return render(request, "pages/compare.html", {"products_compare": products_compare})


def price(request):
    category = Category.objects.all()
    Product.objects.order_by("title")
    maxb = Product.objects.all().aggregate(Max("price"))
    minb = Product.objects.all().aggregate(Min("price"))
    print(maxb["price__max"])
    print(minb)
    if request.method == "POST":

        selectvalue = request.POST.get("selectsort")
        minsalary = request.POST.get("minsalary")
        print(selectvalue)
        if minsalary == "":
            minsalary = minb["price__min"]
        maxsalary = request.POST.get("maxsalary")
        if maxsalary == "":
            maxsalary = maxb["price__max"]

        products_price = Product.objects.filter(
            price__range=(minsalary, maxsalary)
        ).order_by("title")

        return render(
            request,
            "pages/pricetest.html",
            {
                "products_price": products_price,
                "category": category,
                "maxb": maxb,
                "minb": minb,
            },
        )

    else:
        products_price = Product.objects.all().order_by("price")
        print("bjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        return render(
            request,
            "pages/pricetest.html",
            {
                "products_price": products_price,
                "maxb": maxb,
                "minb": minb,
                "category": category,
                "request": request,
            },
        )


def ajaxprice(request, id):
    data = {}
    print("jkhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    if request.POST.get("action") == "post":
        # request.session['currency'] = settings.DEFAULT_CURRENCY
        mint = request.POST.get("mint")
        maxt = request.POST.get("maxt")
        print(mint)
        print(maxt)
        current_user = request.user
        produ = Product.products.filter(category__id=id)
        products = produ.filter(price__range=(mint, maxt))
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total = 0
        for rs in shopcart:
            if rs.product.variant == "None":
                total += rs.product.price * rs.quantity
            else:
                total += rs.variant.price * rs.quantity
        tot = render_to_string("includes/total.html", {"total": total}, request=request)
        c = products.count()
        paginator = Paginator(products, int(c))

        print("cccccccccccccccccc", c)
        page_number = request.GET.get("page")
        products = paginator.get_page(page_number)
        print(type(page_number))
        if page_number == None:
            page_number = "1"

        page_number = int(page_number)
        context = {
            "products": products,
            "maxb": int(maxt),
            "minb": int(mint),
            "number": page_number,
            "request": request,
        }
        context_page = {
            "number": page_number,
            "products": products,
            "request": request,
        }
        data = {
            "rendered_pagination": render_to_string(
                "ajax_pages/paginationproduct.html",
                context=context_page,
                request=request,
            ),
            "rendered_table": render_to_string(
                "ajax_pages/productfilterlist.html", context=context, request=request
            ),
            "tot": tot,
        }

        return JsonResponse(data)
    else:
        mint = 0
        maxt = 10

        maxb = Product.objects.all().aggregate(Max("price"))
        minb = Product.objects.all().aggregate(Min("price"))

        products_price = Product.objects.filter(price__range=(mint, maxt))
        print(products_price)
        context = {
            "products_price": products_price,
            "maxb": maxt,
            "minb": mint,
            "request": request,
        }
        data = {
            "rendered_table": render_to_string(
                "ajax_pages/productfilterlist.html", context=context, request=request
            )
        }

        return JsonResponse(data)
    return JsonResponse(data)