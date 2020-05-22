from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Articles(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False, default="")
    text = db.Column(db.Text, default="")
    image = db.Column(db.String(255), default="")
    topic = db.Column(db.Integer, db.ForeignKey('article_topics.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    published = db.Column(db.Boolean, default=False)
    popular = db.Column(db.Boolean, default=False)
    top_article = db.Column(db.Boolean, default=False)
    editors_pick = db.Column(db.Boolean, default=False)
    
    
    response_fields = {
        "id": fields.Integer,
        "user_id": fields.Integer,
        "title": fields.String,
        "text": fields.String,
        "image": fields.String,
        "topic": fields.String,
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "published": fields.Boolean,
        "popular": fields.Boolean,
        "top_article": fields.Boolean,
        "editors_pick": fields.Boolean,
    }
    
    
    def __init__(self, user_id, title, text, image, topic, published, popular, top_article, editors_pick):
        self.user_id = user_id
        self.title = title
        self.text = text
        self.image = image
        self.topic = topic
        self.published = published
        self.popular = popular
        self.top_article = top_article
        self.editors_pick = editors_pick
        
   
    def __repr__(self):
        return "<Articles %r>" % self.id