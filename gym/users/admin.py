from django.contrib import admin
from .models import CUser
from django.contrib.auth.models import Permission, ContentType

admin.site.register(CUser)
admin.site.register(Permission)
admin.site.register(ContentType)