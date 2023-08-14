from ninja import Router
from .global_auth import GlobalAuth, get_user_token, get_user_refresh_token
from utils.common_schemas import MessageOut
from .schemas.create_user import CreateUserInput, UserOutput
from django.contrib.auth import authenticate
from users.models import CUser
from users.schemas.authentication_schemas import SigninSuccessful, SigninSchema, GetNewTokenInput
from django.shortcuts import get_object_or_404
from jose import jwt
from django.conf import settings
import uuid
from jose import jwt, JWTError

users_controller = Router(tags=['users'])

# Create User EndPoint
@users_controller.post("create_user", auth=GlobalAuth(), response={
    201: MessageOut,
    400: MessageOut,
    401: MessageOut,
    403: MessageOut,
    500: MessageOut,
})
def create_user(request, payload: CreateUserInput):
    
    try: userId = uuid.UUID(request.auth['pk'])
    except Exception as e: return 401, {'message': str(e)}
    
    user: CUser = get_object_or_404(CUser, id = userId)
    
    if not user.has_perm("users.can_add_permission"):
        return 403, {'message': "Not Autherized!, you do not have the permission to add PERMISSIONS."}
    
    if not user.has_perm("users.can_add_group"):
        return 403, {'message': "Not Autherized!, you do not have the permission to add GROUPS."}
    
    
    if user.has_perm("users.can_create_user"):
        
        if payload.permissions != None:
            try: permissions: list = Permission.objects.filter(id__in=payload.permissions)
            except Exception as e: return 500, {"message": f"code: 1, error: {str(e)}"}

        if payload.groups_ids != None:
            try: groups: list = Group.objects.filter(id__in=payload.groups_ids)
            except Exception as e: return 500, {"message": f"code: 2, error: {str(e)}"}
        
        try:
            newUser = CUser.objects.create_user(
                full_name = payload.username,
                username = payload.username,
                email = payload.email,
                age = payload.age,
                password = payload.password
            )
        except Exception as e: return 500, {'message': f"code: 3 => error: {e}"}
        
        
        if payload.permissions != None:
            try: newUser.user_permissions.add(*permissions)
            except Exception as e:
                newUser.delete()
                return 500, {'message': f"code: 4 => error: {e}"}
            
        if payload.groups_ids != None:
            try: newUser.groups.add(groups)
            except Exception as e:
                newUser.delete()
                return 500, {'message': f"code: 5 => error: {e}"}


        return 201, {'message': str(newUser)}
    
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
    
    try:
        return 200, {
            "id": str(user.id),
            "role": str(user),
            "access_token": str(token['access']),
            "refresh_token": str(refresh_token['refresh'])
        }
    except Exception as e:
        return 500, {'message': str(e)}

# -------------------------------

# Get New Token EndPoint
@users_controller.post("get_new_token", response={
    200: SigninSuccessful,
    400: MessageOut,
    401: MessageOut,
    403: MessageOut,
    422: MessageOut,
    500: MessageOut,
})
def get_new_token(request, refresh_token: GetNewTokenInput):
    
    if not refresh_token.token : return 422, {'message': "Token is required!"}
    
    try: user_pk = jwt.decode(token=refresh_token.token, key=settings.SECRET_KEY, algorithms=['HS256'])
    except JWTError as e: return 401, { 'message': 'Unauthorized' }
    
    user: CUser = get_object_or_404(CUser, id = user_pk['pk'])
    
    user_access_token = get_user_token(user)
    user_refresh_token = get_user_refresh_token(user)
    
    return 200, {
        "id": str(user.id),
        "role": "",
        "access_token": str(user_access_token['access']),
        "refresh_token": str(user_refresh_token['refresh'])
    }

# -------------------------------

# Forget Password EndPoint
@users_controller.post("forget_password", response={500: MessageOut})
def forget_password(request):
    return 500, {'message': "Under Development ..."}

# -------------------------------

# Get Users [ With Filter ] EndPoint
@users_controller.get('get_users', auth=GlobalAuth(), response={
    200: list[UserOutput],
    400: MessageOut,
    401: MessageOut,
    403: MessageOut,
    404: MessageOut,
    500: MessageOut
})
def get_users(request, filter: str):
    pass