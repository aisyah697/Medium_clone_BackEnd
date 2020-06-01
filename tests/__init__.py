import pytest, json, logging, hashlib, uuid
from flask import Flask, request, json
from app import cache
from blueprints import db, app
from blueprints.article.model import Articles
from blueprints.article_topic.model import ArticleTopics
from blueprints.user.model import Users

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    # db.drop.all()
    db.create_all()

    salt = uuid.uuid4().hex
    encoded = ('%s%s' % ('password', salt)).encode('utf-8')
    hash_pass = hashlib.sha512(encoded).hexdigest()

    user_internal = Users(full_name="Aisyah Putri Utami", email="aisyah@gmail.com", password=hash_pass, avatar="", status=True, salt=salt)
    # user_internal = session.query(Users).filter(Users.email=="user_internal").one()
    # if user_internal is None:
    #     user_internal = Users(full_name="Aisyah Putri Utami", email="aisyah@gmail.com", password=hash_pass, avatar="", status=True, salt=salt)
    
    user_noninternal = Users(full_name="aaa", email="aaa@gmail.com", password=hash_pass, avatar="", status=True, salt=salt)
    
    db.session.add(user_internal)
    db.session.add(user_noninternal)
    db.session.commit()
    
    article = Articles(user_id=1,
                       title="My Cat",
                       text="Hi, everyone! This is my first post in Medium. Above is my cat. Her name is Lollipop, because she is as sweet as a candy. She’s spoiled, yet so adorable.",
                       image="",
                       image_caption="This is my cat, Lollipop",
                       topic=10,
                       published=True,
                       popular=True,
                       top_article=False,
                       editors_pick=False,
                       )
    
    db.session.add(article)
    db.session.commit()
    
    article_topic = ArticleTopics(topic="Hobbies")
    db.session.add(article_topic)
    db.session.commit()
    
    yield db

    db.drop_all()

def create_token_internal():
    token = cache.get('test-token')
    if token is None:
        data = {
            'email': 'aisyah@gmail.com',
            'password': 'aisyah'
        }
        
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res.json)
        
        assert res.status_code == 200
        
        cache.set('test-token', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token
    
def create_token_noninternal():
    token = cache.get('test-token')
    if token is None:
        data = {
            'email': 'aaa@gmail.com',
            'password': 'aaa'
        }
        
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res.json)
        
        assert res.status_code == 403
        
        cache.set('test-token', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token