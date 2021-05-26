from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm
from django.db.models.aggregates import Avg, Count
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(MPTTModel):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name=_("parent"),
    )
    title = models.CharField(
        max_length=50,
        verbose_name=_("title"),
    )
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to="images/")
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True, allow_unicode=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ["title"]

    # def get_absolute_url(self):
    #     return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        # post.  use __unicode__ in place of
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return " >>> ".join(full_path[::-1])


## class manager to filiter activate product
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(status=True)


class Product(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False"),
    )
    VARIANTS = (
        ("None", "None"),
        ("Size", "Size"),
        ("Color", "Color"),
        ("Size-Color", "Size-Color"),
    )
    Availability = (
        ("Available", "Available"),
        ("Warning", "Warning"),
        ("Not Available", "Not Available"),
    )
    # many to one relation with Category
    category = models.ForeignKey(
        Category,
        related_name="categoryProduct",
        on_delete=models.CASCADE,
        verbose_name=_("category"),
    )
    title = models.CharField(
        max_length=150, blank=True, null=True, verbose_name=_("title")
    )
    # keywords = models.CharField(max_length=255)
    description = RichTextUploadingField(
        blank=True, null=True, verbose_name=_("description")
    )
    image = models.ImageField(
        upload_to="images/",
        default="images/404.png",
        blank=True,
        null=True,
        verbose_name=_("image"),
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name=_("price")
    )

    amount = models.IntegerField(default=0, verbose_name=_("amount"))
    minamount = models.IntegerField(default=1)
    variant = models.CharField(
        max_length=10, choices=VARIANTS, default="None", verbose_name=_("variant")
    )
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    status = models.CharField(max_length=10, choices=STATUS, verbose_name=_("status"))
    create_at = models.DateTimeField(auto_now_add=True)
    startpage = models.BooleanField(default=False, verbose_name=_("start page"))
    update_at = models.DateTimeField(auto_now=True)
    Availability = models.CharField(
        max_length=18,
        choices=Availability,
        default="Available",
        verbose_name=_("Availabiity"),
    )
    like = models.ManyToManyField(User, related_name="favourite", blank=True)
    compare = models.ManyToManyField(User, related_name="compare", blank=True)
    fav = models.BooleanField(default=False)
    objects = models.Manager()
    products = ProductManager()

    def __str__(self):
        return str(self.title)

    def stats(self):
        if self.status == "True":
            return True
        else:
            return False

    stats.boolean = True
    stats.short_description = "status"

    # @property
    # def num_likes(self):
    #     return self.like.all().count()

    # def nlike(self):
    #     d = self.likeproduct.count()
    #     return d
    # nlike.short_description = '#Likes'

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    ####################### this function is used to show state Availability
    def show_availability(self):
        if self.amount > 0:
            return "In The  Stock"
        else:
            return "Out Of The Stock"

    ########################### this function is used to calculate the average of the rating for this product
    def avarege_review(self):
        reviews = Comment.objects.filter(product=self, status="True").aggregate(
            avarage=Avg("rate")
        )
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    ############## this function is used to count comment for this product
    def count_review(self):
        reviews = Comment.objects.filter(product=self, status="True").aggregate(
            count=Count("id")
        )
        counter = 0
        if reviews["count"] is not None:
            counter = int(reviews["count"])
        return counter

    class Meta:
        verbose_name = "ModekklName"
        verbose_name_plural = _("products")


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to="images/")

    def __str__(self):
        return self.title


LIKE_CHOICES = (("like", "like"), ("unlike", "unlike"))


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="likeproduct", on_delete=models.CASCADE
    )
    value = models.CharField(choices=LIKE_CHOICES, default="like", max_length=10)

    def __str__(self):
        return str(self.product)


COMPARE_CHOICES = (("yes", "yes"), ("no", "no"))


class Compare(models.Model):
    user = models.ForeignKey(User, related_name="usercompare", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="compareproduct", on_delete=models.CASCADE
    )
    value = models.CharField(choices=COMPARE_CHOICES, default="yes", max_length=10)

    def __str__(self):
        return self.product


class Comment(models.Model):
    STATUS = (
        ("New", "New"),
        ("True", "True"),
        ("False", "False"),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def stats(self):
        if self.status == "True":
            return True
        else:
            return False

    stats.boolean = True

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["subject", "comment", "rate"]


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe(
                '<p style="background-color:{}">Color </p>'.format(self.code)
            )
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


class ProductLang(models.Model):
    # many to one relation with Category
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # lang = models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True, allow_unicode=True)
    detail = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
