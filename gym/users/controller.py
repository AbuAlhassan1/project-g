from ninja import Router
from .global_auth import GlobalAuth, get_user_token, get_user_refresh_token
from .schemas.common_schemas import MessageOut
from users.schemas.authentication_schemas import SigninSchema, SigninSuccessful
from .schemas.create_user import CreateUserInput
from django.contrib.auth import authenticate
from users.models import CUser
from django.shortcuts import get_object_or_404

users_controller = Router(tags=['users'])

# Create User EndPoint
@users_controller.post("create_user")
def create_user(request):
    user: CUser = request.user
    if user.has_perm("users.can_create_user"):
        return 'he can'
    return "no he can't"

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
@users_controller.post("get_new_token", auth=GlobalAuth())
def get_new_token(request, refresh_token: str):
    pass

# -------------------------------

# Forget Password EndPoint
@users_controller.post("forget_password")
def forget_password(request):
    pass