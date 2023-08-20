from ninja import Schema
from gym.schemas import GymOutput

class CreateUserInput (Schema):
    full_name: str
    age: int
    username: str
    email: str = None
    password: str
    phone: int
    group: str
    
class UserOutput (Schema):
    id: str
    full_name: str
    username: str
    email: str
    phone: int
    gym: GymOutput = None
    
class SigninSchema (Schema):
    username: str = "admin"
    password: str = "admin"
    
class GetNewTokenInput (Schema):
    token: str

class SigninSuccessful (Schema):
    id: str
    role: str
    access_token: str
    refresh_token: str
    gym: GymOutput = None