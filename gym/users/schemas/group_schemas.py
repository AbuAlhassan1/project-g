from ninja import Schema
from .content_type_schemas import ContentTypeOutput

class GroupInput (Schema):
    name: str
    permissions: list
    
class PermissionOutput (Schema):
    id: int
    name: str
    content_type: ContentTypeOutput
    codename: str