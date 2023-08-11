from django.shortcuts import render, get_object_or_404
from ninja import Router
from users.global_auth import GlobalAuth, get_user_token, get_user_refresh_token
from django.contrib.auth.models import Permission, ContentType, Group
from utils.common_schemas import MessageOut
from roles.schemas.group_schemas import PermissionOutput, PermissionInput, GroupInput, GroupOutput
from roles.schemas.content_type_schemas import ContentTypeOutput
import uuid
from users.models import CUser

roles_controller = Router(tags=['roles'])

# Create New Group EndPoint
@roles_controller.post("create_new_group", auth=GlobalAuth(), response={
    201: MessageOut,
    403: MessageOut,
    401: MessageOut,
    500: MessageOut
})
def create_new_group(request, payload: GroupInput):
    # print(request.headers['Authorization'].split(' ')[1])
    userId = uuid.UUID(request.auth['pk'])
    
    user: CUser = get_object_or_404(CUser, id = userId)
    
    if not user.has_perm("users.can_add_group"):
        return 403, {'message': "Not Autherized!, you do not have the permission to add GROUP."}
    
    if payload.permissions != None:
        permissions: list[Permission] = Permission.objects.filter(id__in=payload.permissions)


    try:
        group = Group.objects.create(name = payload.name)
    except Exception as e:
        return 500, {'message': f"code: 1 => error: {e}"}
    
    if payload.permissions != None:
        group.permissions = permissions
        group.save()
    
    return 201, {"message": f"group name: {group}"}

# -------------------------------

# Get All Groups EndPoint
@roles_controller.get("get_all_groups", auth=GlobalAuth(), response={
    200: list[GroupOutput],
    500: MessageOut
})
def get_all_groups(request, name: str = ""):
    try:
        groups = Group.objects.filter(name__contains=name)
    except Exception as e:
        return 500, {'message': f"رزب الكود رقم الزربة 4{e}"}
    
    return 200, groups.all()

# -------------------------------

# Create New Permission EndPoint
@roles_controller.post("create_new_permission", auth=GlobalAuth(), response={
    201: MessageOut,
    403: MessageOut,
    500: MessageOut,
})
def create_new_permission(request, payload: PermissionInput):
    
    userId = uuid.UUID(request.auth['pk'])
    
    user: CUser = get_object_or_404(CUser, id = userId)
    
    if not user.has_perm("users.can_add_permission"):
        return 403, {'message': "Not Autherized!, you do not have the permission to add PERMISSIONS."}
    
    try:
        contentType = ContentType.objects.get(id=payload.content_type)
    except Exception as e:
        return 500, {'message': f"code: 1 => error: {e}"}
    
    try:
        permission = Permission.objects.create(
            name = payload.name,
            content_type = contentType,
            codename = payload.codename
        )
    except Exception as e:
        return 500, {'message': f"code: 1 => error: {e}"}
    
    return 201, {"message": str(permission)}

# -------------------------------

# Get All Permissions EndPoint
@roles_controller.get("get_all_permissions", response={
    200: list[PermissionOutput],
    500: MessageOut
})
def get_all_permissions(request, code_name: str = ""):
    try:
        permissions = Permission.objects.filter(codename__contains=code_name)
    except Exception as e:
        return 500, {'message': f"رزب الكود رقم الزربة 4{e}"}
    
    return 200, permissions

# -------------------------------

# Get Content Type EndPoint
@roles_controller.get("get_content_type", auth=GlobalAuth(), response={
    200: list[ContentTypeOutput],
    500: MessageOut
})
def get_content_type(request):
    try:
        content_types = ContentType.objects.all()
        return 200, content_types
    except Exception as e:
        return 500, {'message': f"زرب الكود رقم الزربة 3 {e}"}
    pass
