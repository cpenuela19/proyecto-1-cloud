# Model to store the document information uploaded by the user

from models.database import db
from marshmallow import fields, Schema
from datetime import datetime

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(512), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="documents")
    embedding = db.relationship("Embedding", back_populates="document", uselist=False, cascade="all, delete-orphan")

class DocumentSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    filename = fields.Str()
    file_url = fields.Str()
    uploaded_at = fields.DateTime()
