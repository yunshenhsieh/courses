# db定義在app的__init__.py內，所以可以這樣import
import pymysql
from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

def _create(username, email):
    user = User(id=1, username=username, email=email)
    db.session.add(user)
    db.session.commit()
    # host = '192.168.125.133'
    # port = 3306
    # user = 'root'
    # passwd = 'example'
    # db = 'mysql'
    # charset = 'utf8mb4'
    # conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    # cursor = conn.cursor()
    # sql_insert = 'INSERT INTO flask_demo (id, username, email) VALUES ({}, "{}", "{}")'.format(1,username,email)
    # cursor.execute(sql_insert)
    # conn.commit()
    # cursor.close()
    # conn.close()
    return

def _update(id, email):
    user = User.query.filter_by(id=id).first()
    user.email = email
    db.session.commit()
    return

def _destroy(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return