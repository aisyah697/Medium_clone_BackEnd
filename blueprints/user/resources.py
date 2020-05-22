from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
import json
from .model import Users
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from blueprints import internal_required
from flask_jwt_extended import get_jwt_claims

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class UserResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('status', location='json', default=True, type=bool)
        
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(args['full_name'], args['email'], hash_pass, args['status'], salt)
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}
    
    @internal_required
    def get(self, id):
        claims = get_jwt_claims()
        qry = Users.query.get(claims['id'])
        
        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404   

    @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('password', location='json', type=str)
        parser.add_argument('avatar', location='json')
        parser.add_argument('bio', location='json')
        parser.add_argument('status', location='json')
        
        args = parser.parse_args()

        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        if args['full_name'] is not None:
            qry.full_name = args['full_name']
        
        if args['email'] is not None:
            qry.email = args['email']
            
        if args['password'] is not None:
            salt = uuid.uuid4().hex
            encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            qry.password = hash_pass
            qry.salt = salt
            
        if args['avatar'] is not None:
            qry.avatar = args['avatar']
            
        if args['bio'] is not None:
            qry.bio = args['bio']
                        
        if args['status'] is not None:
            qry.status = args['status']
            
        db.session.commit()

        return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
        
    @internal_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class UserList(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('full_name'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()

        offset = (args['p'] * args['rp'] - args['rp'])

        qry = Users.query
        if args['orderby'] is not None:
            if args['orderby'] == 'full_name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.full_name))
                else:
                    qry = qry.order_by(Users.full_name)

        rows =[]
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200

api.add_resource(UserList, '', '')
api.add_resource(UserResource, '', '/<id>')