import uuid
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone

class User(Document):
    username = StringField(required=True, unique=True, max_length=10)
    password = StringField(required=True)
    role = StringField(required=True)
    created_time = DateTimeField(default=datetime.now(timezone.utc))

class Project(Document):
    project_id = StringField(default=lambda: str(uuid.uuid4()), unique=True)  # UUID for unique project_id
    name = StringField(required=True)
    description = StringField(required=True, max_length=500)
    created_time = DateTimeField(default=datetime.now(timezone.utc))