from ninja import Schema
from .content_type_schemas import ContentTypeOutput

class GroupInput (Schema):
    name: str
    permissions: list[int] = None

class PermissionOutput (Schema):
    id: int
    name: str
    content_type: ContentTypeOutput
    codename: str

class GroupOutput (Schema):
    id: int
    name: str
    permissions: list[PermissionOutput] = None

class PermissionInput (Schema):
    name: str
    content_type: int
    codename: str