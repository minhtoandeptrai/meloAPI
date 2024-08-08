import re
from flask import json, make_response, request
import mysql.connector
from datetime import datetime
import jwt
class auth_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = 'localhost', user = 'root', password='123123', database='melospace')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('okk')
        except:
            print('fault')
            
    def token_auth(self, endpoints):
        def inner1(func):
            def inner2(*args):
                authorization = request.headers.get("authorization")
                if  re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                    token = authorization.split(" ")[1]
                    try:
                        jwtDecoded = jwt.decode(token, "abc", algorithms = ["HS256"], verify=True,  options={'verify_exp': True})
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR" : "TOKEN_EXPERIED"}, 401)
                    self.cur.execute(f"SELECT roleID from role_endpoint inner join endpoint on role_endpoint.endpointID = endpoint.endpointID where endpointname = '{endpoints}'")
                    result = self.cur.fetchall()
                    print(result)
                    if(len(result) > 0):
                        allowed_role =[item['roleID'] for item in result]
                        print(allowed_role)
                        if 1 == 1 :
                            print('you can access')
                            return func(*args)
                        else: return make_response({'ERROR' :" INVALID_ROLE"})
                    else:
                        print('can not access')
                        return make_response({'ERROR' :" UNKNOW_EDNPOINT"})
                else:
                    return make_response({"ERROR" : "INVALID_TOKEN"}, 401)
            return inner2
        return inner1