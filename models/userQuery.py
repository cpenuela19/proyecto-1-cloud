# Model used to store the user query information

from models.database import db
from marshmallow import fields, Schema
from datetime import datetime

class UserQuery(db.Model):
    __tablename__ = "user_queries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    query_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="queries")

class UserQuerySchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    query_text = fields.Str()
    response_text = fields.Str()
    created_at = fields.DateTime()
