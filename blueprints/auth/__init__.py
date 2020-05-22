from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from functools import wraps

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..user.model import Users
import hashlib

from blueprints import internal_required

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)


class CreateTokenResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()
        
        qry_user = Users.query.filter_by(email=args['email']).first()

        if qry_user is not None:
            user_salt = qry_user.salt
            encoded = ('%s%s' % (args['password'], user_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_user.password:
                qry_user = marshal(qry_user, Users.jwt_client_fields)
                token = create_access_token(identity=args['email'], user_claims=qry_user)
                return {'token': token}, 200
            
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401
        

class RefreshTokenResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200
    
    @jwt_required
    @internal_required
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt_claims()
        token = create_access_token(identity=current_user, user_claims=claims)
        return {'token': token}, 200


api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')