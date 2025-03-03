from models.database import db
from marshmallow import fields, Schema, validate
from datetime import datetime

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(512), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="documents")  # ✅ Eliminado `Embedding`

class DocumentSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(required=True)
    filename = fields.Str(required=True, validate=validate.Length(min=1))
    file_url = fields.Str(required=True)
    uploaded_at = fields.DateTime()
