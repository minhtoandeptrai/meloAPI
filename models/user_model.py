from flask import json, make_response
import mysql.connector
from datetime import datetime, timedelta, timezone
import jwt
import hashlib, time
class user_model:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = "127.0.0.1", user = "root", password="123123", database='melospace')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('connected')
        except:
            print('fault')

    def get_user_by_google_id(self, id):
        try:
            self.cur.execute(f"select * from user where google_id = '{id}'")
        except:
            return 'Fail'
        result = self.cur.fetchall()
        if(len(result) > 0):
            return True
        else: return  False

    def get_user_by_id(self, id):
        print(id)
        if(id):
            try:
                self.cur.execute(f"select * from user where userID = '{id}'")
            except:
                return make_response('fail', 401)

            result = self.cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
        else:
            try:
                self.cur.execute(f"select * from user")
            except:
                return make_response('fail', 401)
            result = self.cur.fetchall()
            if(len(result) > 0):
                return make_response(json.dumps(result), 200)
            else: return  make_response('No data found', 400)
    def register(self, data):

        ## create guid
        current_time = str(time.time())
        name = data['username']
        combined_string = name + current_time
        hash__guid_object = hashlib.sha256(combined_string.encode())
        guid = hash__guid_object.hexdigest()
        
        ##hash password

        hash_pass_object = hashlib.sha256(data['password'].encode())
        hass_password = hash_pass_object.hexdigest()

        print(hass_password)
        ##insert
        try:
            self.cur.execute(f"""
                    INSERT INTO `user`(`UserName`,`Avatar`,`Email`,`Score`,`HassPassWord`,`FullName`,`PhoneNumber`,`guid`) 
                    VALUES('{data['username']}','https://phongreviews.com/wp-content/uploads/2022/11/avatar-facebook-mac-dinh-19.jpg','{data['email']}',
                    50,'{hass_password}','{data['fullname']}','{data['phonenumber']}','{guid}');""")
            return make_response('add susscess',200)
        
        except:
            return make_response('fail', 400)
        

    def register_with_google(self, data):

        ## create guid
        current_time = str(time.time())
        name = data['sub']
        combined_string = name + current_time
        hash__guid_object = hashlib.sha256(combined_string.encode())
        guid = hash__guid_object.hexdigest()
        
        ##insert
        try:
            self.cur.execute(f"""
                    INSERT INTO `user`(`UserName`,`Avatar`,`Email`,`Score`,`FullName`,`guid`,`google_id`) 
                    VALUES('{data['given_name']}','{data['picture']}','{data['email']}',
                    50,'{data['name']}','{guid}', '{data['sub']}');""")
            return make_response('add susscess',200)
        except:
            return make_response('fail', 400)
    def login_user(self, data):
        self.cur.execute(f"""select user.userID, guid, avatar, fullname  from `user` 
                           where username = '{data['username']}' and hasspassword ='{data['password']}'""")
        result = self.cur.fetchall()
        if(len(result) > 0):
            user_data = result[0]
            exp_epoch_time = datetime.now(tz=timezone.utc) + timedelta(days=2)
            _payload = {
                'payload': user_data,
                'exp': exp_epoch_time
            }
            jwt_token = jwt.encode(payload=_payload, key="abc", algorithm="HS256" )
            return make_response({'token' : jwt_token}, 200)
        else: return make_response('Invalid UserName or Password', 400)
    
    def login_user_google(self, id):
        self.cur.execute(f"""select guid, fullname, avatar, google_id from `user` 
                           where google_id = '{id}' """)
        result = self.cur.fetchall()
        user_data = result[0]
        exp_epoch_time = datetime.now(tz=timezone.utc) + timedelta(days=2)
        _payload = {
            'payload': user_data,
            'exp': exp_epoch_time
        }
        jwt_token = jwt.encode(payload=_payload, key="abc", algorithm="HS256" )
        return jwt_token
    
    def update_information(self, data):
        id = data['id']
        isUpdate = False
        if 'username' in data:
            self.cur.execute(f"""
                UPDATE user
                SET username = '{data['username']}'
                WHERE guid = '{id}';
                """)
            isUpdate = True
        if 'thumb' in data:
            self.cur.execute(f"""
                UPDATE user
                SET avatar = '{data['thumb']}'
                WHERE guid = '{id}';
                """)
            isUpdate = True
        if 'fullname' in data:
            self.cur.execute(f"""
                UPDATE user
                SET fullname = '{data['fullname']}'
                WHERE guid = '{id}';
                """)
            isUpdate = True
        if isUpdate == True:
            return make_response('update susscess', 200)
        else: return make_response('Unexpected')