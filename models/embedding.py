# Model used to store the generated vectors for the documents for semantic search

# Model used to reference document embeddings (in-memory FAISS)
from models.database import db
from marshmallow import fields, Schema

class Embedding(db.Model):
    __tablename__ = "embeddings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"), nullable=False, unique=True)
    
    document = db.relationship("Document", back_populates="embedding")

class EmbeddingSchema(Schema):
    id = fields.Int()
    document_id = fields.Int()

