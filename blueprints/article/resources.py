import json, uuid
import werkzeug
import os
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse, inputs
from .model import Articles
from blueprints import db, app
from sqlalchemy import desc
from blueprints import internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.article_topic.model import ArticleTopics
from blueprints.user.model import Users

bp_article = Blueprint('article', __name__)
api = Api(bp_article)

class ArticlebyUser(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    @internal_required
    def get (self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", location='args')

        claims = get_jwt_claims()
        
        args = parser.parse_args()
        qry = Articles.query.filter_by(user_id=claims['id'])
        qry = qry.order_by(desc(Articles.created_at))

        if args['title'] is not None:
            qry = qry.filter_by(name=args['title'])

        rows = []
        for row in qry.all():
            user = Users.query.filter_by(id=row.user_id).first()
            marshalUser = marshal(user, Users.response_fields)
            marshalqry = marshal(row, Articles.response_fields)
            marshalqry["user_id"] = marshalUser
            rows.append(marshalqry)
        return rows, 200

class ArticleResources(Resource):
    def options(self):
        return {'status': 'ok'}, 200
    
    def get(self, id):
        qry = Articles.query.get(id)
        if qry is not None:
            return marshal(qry, Articles.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    @internal_required
    def post(self):
        claims = get_jwt_claims()
        user_fields = Users.query.filter_by(id=claims['id']).first()

        parser = reqparse.RequestParser()
        parser.add_argument('title', location='form', required=True)
        parser.add_argument('text', location='form', required=True)
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('image_caption', location='form')
        parser.add_argument('topic', location='form', default="Hobbies")
        parser.add_argument('published', location='form', type=bool)
        parser.add_argument('popular', location='form', default=False, type=bool)
        parser.add_argument('top_article', location='form', default=False, type=bool)
        parser.add_argument('editors_pick', location='form', default=False, type=bool)
        
        args = parser.parse_args()

        UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

        image = args['image']

        if image:
                randomstr = uuid.uuid4().hex 
                filename = randomstr+'_'+image.filename
                image.save(os.path.join(UPLOAD_FOLDER, filename))
                img_path = UPLOAD_FOLDER.replace('./', '/')+'/'+filename
     
        article_topic = ArticleTopics.query.filter_by(topic = args['topic']).first()
        if article_topic is None:
            return {"message": "Topic is not found"}, 404, {'Content-Type': 'application/json'}
     
        article = Articles(user_fields.id,
                           args['title'],
                           args['text'],
                        #    args['image'],
                           filename,
                           args['image_caption'],
                           article_topic.id,
                           args['published'],
                           args['popular'],
                           args['top_article'],
                           args['editors_pick'])
        
        db.session.add(article)
        db.session.commit()
        app.logger.debug('DEBUG: %s', article)

        return marshal(article, Articles.response_fields), 200, {'Content-Type': 'application/json'} 

    @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', location='form')
        parser.add_argument('text', location='form')
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('image_caption', location='form')
        parser.add_argument('topic', location='form')
        parser.add_argument('published', location='form', type=bool)
        parser.add_argument('popular', location='form', default=False, type=bool)
        parser.add_argument('top_article', location='form', default=False, type=bool)
        parser.add_argument('editors_pick', location='form', default=False, type=bool)
        
        args = parser.parse_args()

        qry = Articles.query.get(id)
        if qry is None:
            return {'status':'NOT_FOUND'}, 404
        
        if args['title'] is not None:
            qry.title = args['title']
          
        if args['text'] is not None:
            qry.text = args['text'] 
            
        if args['image'] is not None:
            UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
            image = args['image']
            if image:
                randomstr = uuid.uuid4().hex 
                filename = randomstr+'_'+image.filename
                image.save(os.path.join(UPLOAD_FOLDER, filename))
                img_path = UPLOAD_FOLDER.replace('./', '/')+'/'+filename
                qry.image = filename
            
        if args['image_caption'] is not None:
            qry.image_caption = args['image_caption']
        
        if args['topic'] is not None:
            article_topic = ArticleTopics.query.filter_by(topic = args['topic']).first()
            if article_topic is not None:
                qry.category = article_topic.id
        
        if args['published'] is not None:
            qry.published = args['published']
            
        if args['popular'] is not None:
            qry.popular = args['popular']
            
        if args['top_article'] is not None:
            qry.top_article = args['top_article']
            
        if args['editors_pick'] is not None:
            qry.editors_pick = args['editors_pick']
        
        db.session.commit()

        return marshal(qry, Articles.response_fields), 200
    
    @internal_required
    def delete(self, id):
        qry = Articles.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200


class ArticleList(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('title'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc','asc'))
        
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        
        qry = Articles.query.order_by(desc(Articles.created_at))
        qry = qry.order_by(desc(Articles.updated_at))
        
        if args['orderby'] is not None:
            if args['orderby'] == 'title':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Articles.title))
                else:
                    qry = qry.order_by(Articles.title)
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            user = Users.query.get(row.user_id)
            marshalUser = marshal(user, Users.response_fields)
            marshalqry = marshal(row, Articles.response_fields)
            marshalqry["user"] = marshalUser
            rows.append(marshalqry)
        
        return rows, 200
    
    
class PopularArticle(Resource):
    def options(self, id=None):
        return {'status':'ok'},200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args', help='invalid orderby value', choices=['title'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Articles.query.filter_by(published=True)
        qry = qry.filter_by(popular=True)
        qry = qry.order_by(desc(Articles.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'title':
                qry = qry.order_by(Articles.title)
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            user = Users.query.get(row.user_id)
            marshalUser = marshal(user, Users.response_fields)
            marshalqry = marshal(row, Articles.response_fields)
            marshalqry["user"] = marshalUser
            rows.append(marshalqry)
        return rows, 200


class TopArticle(Resource):
    def options(self, id=None):
        return {'status':'ok'},200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args', help='invalid orderby value', choices=['title'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Articles.query.filter_by(published=True)
        qry = qry.filter_by(top_article=True)
        qry = qry.order_by(desc(Articles.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'title':
                qry = qry.order_by(Articles.title)
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            user = Users.query.get(row.user_id)
            marshalUser = marshal(user, Users.response_fields)
            marshalqry = marshal(row, Articles.response_fields)
            marshalqry["user"] = marshalUser
            rows.append(marshalqry)
        return rows, 200
    
    
class EditorsPickArticle(Resource):
    def options(self, id=None):
        return {'status':'ok'},200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=20)
        parser.add_argument('order_by', location='args', help='invalid orderby value', choices=['title'])

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        qry = Articles.query.filter_by(published=True)
        qry = qry.filter_by(editors_pick=True)
        qry = qry.order_by(desc(Articles.created_at))
        if args['order_by'] is not None:
            if args['order_by'] == 'title':
                qry = qry.order_by(Articles.title)
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            user = Users.query.get(row.user_id)
            marshalUser = marshal(user, Users.response_fields)
            marshalqry = marshal(row, Articles.response_fields)
            marshalqry["user"] = marshalUser
            rows.append(marshalqry)
        return rows, 200


api.add_resource(ArticlebyUser, '/user')
api.add_resource(ArticleList, '', '/list')
api.add_resource(ArticleResources, '', '/<id>')
api.add_resource(PopularArticle, '/popular')
api.add_resource(TopArticle, '/top')
api.add_resource(EditorsPickArticle, '/editorspicks')
