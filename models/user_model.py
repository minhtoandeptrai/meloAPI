from flask import json, make_response
import mysql.connector
from datetime import datetime, timedelta, timezone
import jwt
import hashlib, time
import app
class user_model:

    def get_user_by_google_id(self, id):
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"select * from user where google_id = '{id}'")
            result = cur.fetchall()
            if(len(result) > 0):
                return True
            else: return  False

        except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    
        
    def get_user_by_id(self, id):

        if(id):
            try:
                conn = app.get_db_connection()
                cur = conn.cursor(dictionary=True)
                cur.execute(f"select * from user where userID = '{id}'")
                result = cur.fetchall()
                if(len(result) > 0):
                    return make_response(json.dumps(result), 200)
                else: return  make_response('No data found', 400)
            except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
            finally:
                cur.close()
                conn.close()

            
        # else:
        #     try:
        #         cur.execute(f"select * from user")
        #     except:
        #         return make_response('fail', 401)
        #     result = self.cur.fetchall()
        #     if(len(result) > 0):
        #         return make_response(json.dumps(result), 200)
        #     else: return  make_response('No data found', 400)
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
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                    INSERT INTO `user`(`UserName`,`Avatar`,`Email`,`Score`,`HassPassWord`,`FullName`,`PhoneNumber`,`guid`) 
                    VALUES('{data['username']}','https://phongreviews.com/wp-content/uploads/2022/11/avatar-facebook-mac-dinh-19.jpg','{data['email']}',
                    50,'{hass_password}','{data['fullname']}','{data['phonenumber']}','{guid}');""")
            conn.commit()
            
            return make_response('add susscess',200)
        except Exception as e:
            print(f"An error occurred: {e}")
            return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
        

    def register_with_google(self, data):

        ## create guid
        current_time = str(time.time())
        name = data['sub']
        combined_string = name + current_time
        hash__guid_object = hashlib.sha256(combined_string.encode())
        guid = hash__guid_object.hexdigest()
        
        ##insert
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""
                    INSERT INTO `user`(`UserName`,`Avatar`,`Email`,`Score`,`FullName`,`guid`,`google_id`) 
                    VALUES('{data['given_name']}','{data['picture']}','{data['email']}',
                    50,'{data['name']}','{guid}', '{data['sub']}');""")
            conn.commit()
            
            return make_response('add susscess',200)
        except Exception as e:
            print(f"An error occurred: {e}")
            return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    def login_user(self, data):
        try:
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""select user.userID, guid, avatar, fullname  from `user` 
                            where username = '{data['username']}' and hasspassword ='{data['password']}'""")
            result = cur.fetchall()
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    
    def login_user_google(self, id):
        try: 
            conn = app.get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute(f"""select guid, fullname, avatar, google_id from `user` 
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
        except Exception as e:
            print(f"An error occurred: {e}")
            return make_response('fail', 400)
        finally:
            cur.close()
            conn.close()
    def update_information(self, data):
        id = data['id']
        isUpdate = False
        if 'username' in data:
            try:
                conn = app.get_db_connection()
                cur = conn.cursor(dictionary=True)
                cur.execute(f"""
                    UPDATE user
                    SET username = '{data['username']}'
                    WHERE guid = '{id}';
                    """)
                conn.commit()
                
                isUpdate = True
            except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
            finally:
                cur.close()
                conn.close()
        if 'thumb' in data:
            try: 
                conn = app.get_db_connection()
                cur = conn.cursor(dictionary=True)
                cur.execute(f"""
                    UPDATE user
                    SET avatar = '{data['thumb']}'
                    WHERE guid = '{id}';
                    """)
                conn.commit()
                
                isUpdate = True
            except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
            finally:
                cur.close()
                conn.close()
        if 'fullname' in data:
            try: 
                conn = app.get_db_connection()
                cur = conn.cursor(dictionary=True)
                cur.execute(f"""
                    UPDATE user
                    SET fullname = '{data['fullname']}'
                    WHERE guid = '{id}';
                    """)
                conn.commit()
                
                isUpdate = True
            except Exception as e:
                print(f"An error occurred: {e}")
                return make_response('fail', 400)
            finally:
                cur.close()
                conn.close()
        if isUpdate == True:
            return make_response('update susscess', 200)
        else: return make_response('Unexpected')