from ninja import Schema

class CreateUserInput (Schema):
    full_name: str
    username: str
    password: str
    phone: int
    role: int