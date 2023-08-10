from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from users.controller import users_controller
from roles.controller import roles_controller

api = NinjaAPI()

api.add_router("users", users_controller)
api.add_router("roles", roles_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]