from ninja import Schema
from uuid import UUID

class SigninSchema (Schema):
    username: str = "admin"
    password: str = "admin"

class SigninSuccessful (Schema):
    id: str
    role: str
    access_token: str
    refresh_token: str