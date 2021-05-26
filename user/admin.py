from django.contrib import admin

from user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone',
                    'city', 'country',  'image_tag']
    # readonly_fields = ('image_tag',)


admin.site.register(UserProfile, UserProfileAdmin)
