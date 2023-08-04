from ninja import Schema

class CreateUserInput (Schema):
    full_name: str
    age: int
    username: str
    email: str = None
    password: str
    phone: str
    group_id: int = None
    permissions: list = None