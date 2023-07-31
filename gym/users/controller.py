from ninja import Router
from .global_auth import GlobalAuth, get_user_token, get_user_refresh_token
from .schemas.common_schemas import MessageOut
from users.schemas.authentication_schemas import SigninSchema, SigninSuccessful
from .schemas.create_user import CreateUserInput
from .schemas.group_schemas import PermissionOutput
from .schemas.content_type_schemas import ContentTypeOutput
from django.contrib.auth import authenticate
from users.models import CUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, ContentType
from jose import jwt
from django.conf import settings

users_controller = Router(tags=['users'])

# Create User EndPoint
@users_controller.post("create_user", response={
    201: MessageOut,
    500: MessageOut
})
def create_user(request, payload: CreateUserInput):
    
    user: CUser = request.user
    
    if user.has_perm("users.can_create_user"):
        
        try:
            user = CUser.objects.create_user()
            user.groups.add
        except Exception as e:
            return 500, {'message': f"زرب الكود ,رقم الزربة 2 {e}"}
        
        return 'he can'
    
    
    return 403, {'message': "Not Autherized!"}

# -------------------------------

# Sign in EndPoint
@users_controller.post("signin", response = {
    200: SigninSuccessful,
    500: MessageOut,
    400: MessageOut,
    401: MessageOut,
})
def signin(request, payload: SigninSchema):
    if not payload.username:
        return 400, {'message': "Username field required!"}
    elif not payload.password:
        return 400, {'message': "Password field required!"}
    elif not payload.username and not payload.password:
        return 400, {'message': "Username and Password fields are required!"}
    
    try:
        user: CUser = authenticate(username=payload.username, password=payload.password)
    except Exception as e:
        return 500, {'message': f"زرب الكود -_- | رقم الزربة 1 {e}"}
    
    if not user:
        return 401, {'message': "Wrong username or password!"}

    # Everything Just Fine [ generate token & refresh token and return the response. ] ...
    token = get_user_token(user)
    refresh_token = get_user_refresh_token(user)
    
    return 200, {
        "id": user.id,
        "role": str(user),
        "access_token": str(token['access']),
        "refresh_token": str(refresh_token['refresh'])
    }

# -------------------------------

# Get New Token EndPoint
@users_controller.post("get_new_token", response={
    200: SigninSuccessful,
    500: MessageOut,
    403: MessageOut
})
def get_new_token(request, refresh_token: str):
    
    try:
        tokent_info = jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        return 403, {'message': str(e)}
    
    try:
        user = request.user
    except Exception as e:
        return 500, {'message': f"{e}"}
    
    user_access_token = get_user_token(user)
    user_refresh_token = get_user_refresh_token(user)
    
    return 200, {
        "id": user.id,
        "role": "",
        "access_token": str(user_access_token['access']),
        "refresh_token": str(user_refresh_token['refresh'])
    }

# -------------------------------

# Forget Password EndPoint
@users_controller.post("forget_password")
def forget_password(request):
    pass

# -------------------------------

# Create New Group EndPoint
@users_controller.post("create_new_group", auth=GlobalAuth())
def create_new_group(request, payload):
    pass

# -------------------------------

# Create New Permission EndPoint
@users_controller.post("create_new_permission", auth=GlobalAuth())
def create_new_permission(request, payload):
    pass

# -------------------------------

# Get All Permissions EndPoint
@users_controller.get("get_all_permissions", auth=GlobalAuth(), response={
    200: list[PermissionOutput],
    500: MessageOut
})
def get_all_permissions(request):
    try:
        permissions = Permission.objects.all()
    except Exception as e:
        return 500, {'message': f"رزب الكود رقم الزربة 4{e}"}
    
    return 200, permissions

# -------------------------------

# Get Content Type EndPoint
@users_controller.get("get_content_type", auth=GlobalAuth(), response={
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
