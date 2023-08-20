from ninja import Schema

class ContentTypeOutput (Schema):
    id: int
    app_label: str
    model: str