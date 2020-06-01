from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255))
    avatar = db.Column(db.String(255), default="")
    bio = db.Column(db.String(255), default="")
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    deleted_at = db.Column(db.DateTime)
    article = db.relationship('Articles', backref='users', lazy=True, uselist=False)

    response_fields = {
        'id': fields.Integer,
        'full_name': fields.String,
        'email': fields.String,
        'password': fields.String,
        'avatar': fields.String,
        'bio': fields.String,
        'status': fields.Boolean,
    }

    jwt_client_fields = {
        'id': fields.Integer,
        'full_name': fields.String,
        'email': fields.String,
        'avatar': fields.String,
        'status': fields.Boolean,
        
    }

    def __init__(self, full_name, email, password, avatar, status, salt):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.avatar = avatar
        self.status = status
        self.salt = salt

    def __repr__(self):
        return '<Users %r>' % self.id