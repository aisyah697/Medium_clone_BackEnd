from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class ArticleTopics(db.Model):
    __tablename__ = "article_topics"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),onupdate=func.now()) 
    article_id = db.relationship('Articles', backref='article_topics', lazy=True) 
    
    response_fields = {
        'id': fields.Integer,
        'topic': fields.String
    }
    
    def __init__(self, topic):
        self.topic = topic
    
    
    def __repr__(self):
        return "<ArticleTopics %r>" % self.id