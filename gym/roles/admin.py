from django.contrib import admin
from users.models import CUser
from django.contrib.auth.models import Permission, ContentType

# Register your models here.
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(CUser.user_permissions.through)
admin.site.register(CUser.groups.through)