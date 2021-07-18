from django.contrib import admin
from order.models import ShopCart, OrderProduct, Order
import csv
from django.http import HttpResponse
import datetime
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)

    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"

# to see order detail
def order_detail(obj):
    url = reverse("admin_order_detail", args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    url = reverse("admin_order_pdf", args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = "Invoice"


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    # readonly_fields = ("product", "price", "quantity", "amount")
    # can_delete = False
    extra = 1
    raw_id_fields = ["product"]


class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "user",
        "first_name",
        "phone",
        "city",
        "status",
        "create_at",
        "paid",
        order_detail,
        order_pdf,
    ]
    # list_filter = ['status']
    list_per_page = 20
    # list_filter = (
    #     # for ordinary fields
    #     # ('title', DropdownFilter),
    #     # ('status', DropdownFilter),
    #     # for choice fields
    #     ('status', ChoiceDropdownFilter),
    #     ('update_at', DateRangeFilter)
    #     # for related fields
    #     # ('status', RelatedDropdownFilter),
    # )
    ordering = ("id",)
    readonly_fields = (
        "address",
        "city",
        "country",
        "phone",
        "first_name",
        "ip",
        "last_name",
        "phone",
        "city",
    )
    # can_delete = False
    actions = [export_to_csv]

    inlines = [OrderProductline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "price",
        "quantity",
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)