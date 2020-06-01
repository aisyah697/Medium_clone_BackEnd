import hashlib
from datetime import timedelta
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims

import json, config, os, jwt
from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS


app = Flask(__name__)

CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)

flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == "Production":
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['status']:
            return {'status': 'FORBIDDEN', 'message': 'Internal only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

@app.before_request
def before_request():
    path = request.path.split('/')
    if request.method == "GET" and path[1] == "img" : 
        return send_from_directory("."+app.config['UPLOAD_FOLDER'], path[2]), 200

@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else :
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods':'*'}

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    try:
        if response.status_code == 200:
            app.logger.warning("REQUEST_LOG\t%s", json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
        else:
            app.logger.error("REQUEST_LOG\t%s", json.dumps({
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
    except Exception as e:
        pass
    return response



from blueprints.auth import bp_auth
app.register_blueprint(bp_auth, url_prefix='/auth')

from blueprints.user.resources import bp_user
app.register_blueprint(bp_user, url_prefix='/user')

from blueprints.article.resources import bp_article
app.register_blueprint(bp_article, url_prefix='/article')

from blueprints.article_topic.resources import  bp_article_topic
app.register_blueprint(bp_article_topic, url_prefix='/article_topic')


db.create_all()