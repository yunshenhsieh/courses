from flask_restful import Resource, reqparse
from flask import jsonify, make_response
import pymysql
import traceback

from restful_api_server.server import db
from restful_api_server.models import UserModel
# 沒用jsonify轉換，直接return dict()，headers中的content-type也是application/Json

# 檢查post傳來的資料，有設定的才收，沒設定的就都不留
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('email')

class User(Resource):
    def db_init(self):
        db = pymysql.connect(host='192.168.125.133',
                             port=3306, user='root',
                             passwd='example',
                             db='mysql',
                             charset='utf8mb4')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = 'Select * From flask_demo_2 Where id = {} and deleted is not True;'.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()
        return jsonify({'data': user})

    def patch(self, id):
        # db, cursor = self.db_init()
        # arg = parser.parse_args()
        # user = {
        #     'id': arg['id'],
        #     'username': arg['username'],
        #     'email': arg['email']
        # }
        # query = []
        # for key, value in user.items():
        #     if value != None:
        #         query.append(key + " = " + "'{}'".format(value))
        # query = ','.join(query)
        # sql = 'Update flask_demo_2 Set {} Where id = {};'.format(query, id)
        # response = {}
        # try:
        #     cursor.execute(sql)
        #     response['msg'] = 'success'
        # except:
        #     traceback.print_exc()
        #     response['msg'] = 'failed'
        #
        # db.commit()
        # db.close()
        # return jsonify(response)

        #下方為SQLAlchemy的寫法
        arg = parser.parse_args()
        user = UserModel.query.filter_by(id=id, deleted=None).first()
        if arg['username'] != None:
            user.name = arg['username']

        response = {}
        try:
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response)

    def delete(self, id):
        db, cursor = self.db_init()
        # 下行為硬刪除
        # sql = 'Delete From flask_demo_2 Where id = {};'.format(id)
        # 下行為軟刪除
        sql = 'Update flask_demo_2 Set deleted = True Where id = {};'.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)

        # 下方為SQLAlchemy的寫法，硬刪除
        # user = UserModel.query.filter_by(id=id, deleted=None).first()
        #
        # response = {}
        # try:
        #     db.session.delete(user)
        #     db.session.commit()
        #     response['msg'] = 'success'
        # except:
        #     traceback.print_exc()
        #     response['msg'] = 'failed'
        # return jsonify(response)

class Users(Resource):
    def db_init(self):
        db = pymysql.connect(host='192.168.125.133',
                             port=3306, user='root',
                             passwd='example',
                             db='mysql',
                             charset='utf8mb4')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        # db, cursor = self.db_init()
        # sql = 'Select * From flask_demo_2 Where deleted is not True;'
        # # 下面3行為有條件的搜尋
        # arg = parser.parse_args()
        # if arg['username'] != None:
        #     sql =sql.replace(';','') + ' and username = "{}";'.format(arg['username'])
        #
        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()
        # return jsonify({'data': users})

        #下方為SQLAlchemy的寫法
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})

    def post(self):
        # db, cursor = self.db_init()
        # arg = parser.parse_args()
        # user = {
        #     'id': arg['id'],
        #     'username': arg['username'],
        #     'email': arg['email'] or 0
        # }
        # sql = 'Insert into flask_demo_2(id, username, email) values ({}, "{}", "{}");'\
        #     .format(user['id'], user['username'], user['email'])
        #
        # response = {}
        # status_code = 200
        # try:
        #     cursor.execute(sql)
        #     response['msg'] = 'success'
        # except:
        #     status_code = 400
        #     traceback.print_exc()
        #     response['msg'] = 'failed'
        #
        # db.commit()
        # db.close()
        # return make_response(jsonify(response), status_code)

        # 下方為SQLAlchemy的寫法
        arg = parser.parse_args()
        user = {
            'id': arg['id'],
            'username': arg['username'],
            'email': arg['email'] or 0
        }
        response = {}
        status_code = 200

        try:
            new_user = UserModel(name=user['username'], email=user['email'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'

        return make_response(jsonify(response), status_code)