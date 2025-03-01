from models.database import db
from marshmallow import fields, Schema, validate
import hashlib

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    documents = db.relationship("Document", back_populates="user", cascade="all, delete-orphan")
    queries = db.relationship("UserQuery", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
