from ninja import Schema

class CreateUserInput (Schema):
    full_name: str
    age: int
    username: str
    email: str = None
    password: str
    phone: str
    groups_ids: list[int] = None
    permissions: list[int] = None
    
class UserOutput (Schema):
    id: str
    full_name: str
    username: str
    email: str
    phone: int
    