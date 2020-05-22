from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(255), default="")
    description = db.Column(db.String(255), default="")
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    
    response_fields = {
        "id": fields.Integer,
        "image": fields.String,
        "description": fields.String,
        "article_id": fields.Integer,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
    }
    
    def __init__(self, image, article_id):
        self.image = image
        self.article_id = article_id
    
    
    def __repr__(self):
        return "<Articles %r>" % self.id
    