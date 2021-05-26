from django.contrib import admin
from .models import Category, Product, Images, Comment, Color, Size, Variants
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    RelatedDropdownFilter,
    ChoiceDropdownFilter,
)

# Register your models here.


class CategoryAdmin2(ImportExportModelAdmin, DraggableMPTTAdmin):

    mptt_indent_field = "title"
    list_display = (
        "tree_actions",
        "indented_title",
        "related_products_count",
        "related_products_cumulative_count",
    )
    list_display_links = ("indented_title", "related_products_count")

    prepopulated_fields = {
        "slug": ("title",),
        "title_en": ("title",),
        "slug_en": ("title",),
        "slug_ar": ("title_ar",),
    }
    # inlines = [CategoryLangInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, "category", "products_cumulative_count", cumulative=True
        )

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
            qs, Product, "category", "products_count", cumulative=False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = (
        "Related products (for this specific category)"
    )

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = "Related products (in tree)"


################# show multi images for one product ################################
@admin_thumbnails.thumbnail("image")
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ("id",)
    extra = 1
    classes = ("collapse",)


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ("image_tag",)
    extra = 1
    show_change_link = True
    classes = ("collapse",)


class ProductAdmin(ImportExportModelAdmin):

    list_display = [
        "title",
        "category",
        "stats",
        "startpage",
        "image_tag",
        "price",
        "ago",
    ]
    # list_editable = ("price",)
    list_display_links = ("title", "image_tag")

    list_filter = (
        ("category", RelatedDropdownFilter),
        ("title", DropdownFilter),
        ("status"),
        ("startpage"),
    )

    # ordering = ('-price', 'title',)
    # search_fields = ('title',)
    # readonly_fields = ("image_tag",)
    # # actions = None
    actions = (
        "duplicate_event",
        "show_start_page",
        "hide_start_page",
        "make_status_enable",
        "make_status_disable",
    )
    # # raw_id_fields = ('category',)

    def duplicate_event(self, request, queryset):
        # queryset.update(status=False)
        count = 0
        for object in queryset:
            object.id = None
            object.status = False
            # object.slug = 'rlv'
            count += 1
            object.save()
        if count > 1:
            self.message_user(request, f"{count} Products is Duplicated ")
        else:
            self.message_user(request, f"{count} Product is Duplicated ")

    duplicate_event.short_description = "Copy "

    def show_start_page(self, request, queryset):
        queryset.update(startpage=True)
        count = 0
        for object in queryset:

            count += 1

        if count > 1:
            self.message_user(
                request, f"{count} Products Is Showing In The Start Page "
            )
        else:
            self.message_user(request, f"{count} Product Is Showing In The Start Page ")

    show_start_page.short_description = "Show In The Start Page"

    def hide_start_page(self, request, queryset):
        queryset.update(startpage=False)
        count = 0
        for object in queryset:

            count += 1

        if count > 1:
            self.message_user(
                request, f"{count} Products are Hiding from The Start Page "
            )
        else:
            self.message_user(
                request, f"{count} Product Is Hiding from The Start Page "
            )

    hide_start_page.short_description = "Hide from Start Page "

    def make_status_enable(self, request, queryset):
        queryset.update(status=True)
        count = 0
        for object in queryset:

            count += 1

        if count > 1:
            self.message_user(request, f"{count} Products are make status enable ")
        else:
            self.message_user(request, f"{count} Product Is make status enable ")

    make_status_enable.short_description = "make status enable"

    def make_status_disable(self, request, queryset):
        queryset.update(status=False)
        count = 0
        for object in queryset:

            count += 1

        if count > 1:
            self.message_user(request, f"{count} Products are make status disable ")
        else:
            self.message_user(request, f"{count} Product Is make status disable ")

    make_status_disable.short_description = "make status disable"

    def ago(self, Product):
        ag = timezone.now() - Product.update_at
        return ag.days

    inlines = [
        ProductImageInline,
        ProductVariantsInline,
    ]
    prepopulated_fields = {
        "slug": ("title_en",),
        "title": ("title_en",),
        "slug_en": ("title_en",),
        "slug_ar": ("title_ar",),
        # "description_en": ("description",),
    }
    list_per_page = 20
    # date_hierarchy = 'create_at'

    fieldsets = (
        (
            "English",
            {"classes": ("",), "fields": ("title_en", "description_en")},
        ),
        (
            "Arabic",
            {"classes": ("",), "fields": ("title_ar", "description_ar")},
        ),
        (
            "Setting Product",
            {
                "classes": ("",),
                "fields": (
                    "category",
                    "price",
                    "variant",
                    "amount",
                    "minamount",
                    "image",
                    "image_tag",
                    "status",
                ),
            },
        ),
        (
            None,
            {
                "classes": ("empty-form",),
                "fields": ("slug", "slug_en", "slug_ar", "title"),
            },
        ),
    )
    readonly_fields = ("image_tag",)
    # def action_btn(self, obj):

    #     html = "<a class='btn btn-danger'style='padding:6px; margin: 0px 6px;color:#f1c40f;' href='/admin/product/product/" + \
    #         str(obj.id)+"/change/'><i class='fa fa-eye' style='display:inline;'></i></a>"
    #     html += "<a class='btn btn-danger'style='padding:6px; margin: 0px 6px;color:#e74c3c;' href='/admin/product/product/" + \
    #         str(obj.id)+"/delete/'><i class='fa fa-trash' style='display:inline;'></i></a>"

    #     return format_html(html)
    # action_btn.short_description = "Action"
    # action_btn.allow_tags = True
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
    # actions = ["export_as_csv"]

    # def export_as_csv(self, request, queryset):
    #     pass

    # export_as_csv.short_description = "Export Selected"

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class CommentAdmin(admin.ModelAdmin):
    list_display = ["subject", "comment", "status", "create_at", "stats"]
    list_filter = ["status"]
    # readonly_fields = ('subject', 'comment',)
    search_fields = ("comment",)
    readonly_fields = ("subject", "comment", "ip", "user", "product", "rate", "id")


class ColorAdmin(ImportExportModelAdmin):
    list_display = ["name", "code", "color_tag"]


class SizeAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]


class VariantsAdmin(ImportExportModelAdmin):
    list_display = [
        "title",
        "product",
        "color",
        "size",
        "price",
        "quantity",
        "image_tag",
    ]


class ImagesAdmin(ImportExportModelAdmin):
    list_display = ["title", "image", "product"]


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Variants, VariantsAdmin)