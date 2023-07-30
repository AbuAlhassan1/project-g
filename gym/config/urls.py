from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from users.controller import users_controller

api = NinjaAPI()

api.add_router("users", users_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]