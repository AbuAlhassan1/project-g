from ninja import Schema

class GymOutput ( Schema):
    id: int
    name: str
    description: str
    location: str