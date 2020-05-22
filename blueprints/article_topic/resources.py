from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import ArticleTopics
import hashlib
import uuid
from blueprints import internal_required
from blueprints import db, app

bp_article_topic = Blueprint('article_topic', __name__)
api = Api(bp_article_topic)


class ArticleTopicList(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = ArticleTopics.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, ArticleTopics.response_fields))

        return rows, 200


class ArticleTopicResources(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('topic', location='json', required=True)
        
        args = parser.parse_args()

        article_topic = ArticleTopics(args['topic'])
        db.session.add(article_topic)
        db.session.commit()

        app.logger.debug('DEBUG : %s', article_topic)

        return marshal(article_topic, ArticleTopics.response_fields), 200, {'Content-Type': 'application/json'}


    def get(self, id):
        qry = ArticleTopics.query.get(id)
        if qry is not None:
            return marshal(qry, ArticleTopics.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404


    @internal_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('topic', location='json')
        args = parser.parse_args()

        qry = ArticleTopics.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        if args['topic'] is not None:
            qry.topic = args['topic']

        db.session.commit()

        return marshal(qry, ArticleTopics.response_fields), 200

    @internal_required
    def delete(self, id):
        qry = ArticleTopics.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()
        return {'status': 'DELETED'}, 200


api.add_resource(ArticleTopicList, '')
api.add_resource(ArticleTopicResources, '', '/<id>')
