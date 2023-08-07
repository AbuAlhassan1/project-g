from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CUser
from django.contrib.auth.models import Permission, ContentType

admin.site.register(CUser, UserAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(CUser.user_permissions.through)
admin.site.register(CUser.groups.through)