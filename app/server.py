import json
import time

from flask import Flask, g

from app.mysql.db import MySQLDB
from app.redis.redis import RedisKV

app = Flask(__name__)

REDIS_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': 6379
}

MYSQL_CONFIG = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'admin',
    'PASS': 'foobar',
    'DB': 'test'
}


mysql_db = MySQLDB.from_dict(MYSQL_CONFIG)
redis_kv = RedisKV.from_dict(REDIS_CONFIG)


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    diff = time.time() - g.start
    r = json.loads(response.get_data())
    r['time'] = diff
    response.set_data(json.dumps(r))
    return response

################# REDIS ROUTES

@app.route("/redis/<int:id>", methods=['POST'])
def hello_redis(id):
    global redis_kv
    redis_kv.get_count(id)
    return {
        'success': True
    }

@app.route("/redis/<int:id>/decrement", methods=['POST'])
def hello_redis_decrement(id):
    global redis_kv
    redis_kv.decrement_count(id)
    return {
        'success': True
    }

@app.route("/redis/<int:id>/increment", methods=['POST'])
def hello_redis_increment(id):
    global redis_kv
    redis_kv.increment_count(id)
    return {
        'success': True
    }

################# MYSQL ROUTES

@app.route("/mysql/<int:id>", methods=['POST'])
def hello_mysql(id):
    global mysql_db
    mysql_db.get_count(id)
    return {
        'success': True
    }

@app.route("/mysql/<int:id>/decrement", methods=['POST'])
def hello_mysql_dec(id):
    global mysql_db
    mysql_db.decrement_count(id)
    return {
        'success': True
    }

@app.route("/mysql/<int:id>/increment", methods=['POST'])
def hello_mysql_inc(id):
    global mysql_db
    mysql_db.increment_count(id)
    return {
        'success': True
    }
