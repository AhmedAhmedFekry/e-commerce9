from django.contrib import admin
import admin_thumbnails
from home.models import Setting, ContactMessage, Offer, FAQ
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "update_at", "status"]

    readonly_fields = ("name", "subject", "email", "message", "ip")
    list_filter = ["status"]


class OfferAdmin(admin.ModelAdmin):
    list_display = ["name", "link", "image_tag"]


class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "ordernumber", "status"]
    list_filter = [
        "status",
    ]


class SettingAdmin(ImportExportModelAdmin):
    list_display = [
        "title",
    ]


admin.site.register(Setting, SettingAdmin)

admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(FAQ, FAQAdmin)