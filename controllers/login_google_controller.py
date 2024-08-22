from app import app
from models.user_model import user_model
from flask import request, jsonify, make_response
import requests
@app.route('/google_login', methods=['POST'])
def login():
    auth_code = request.get_json()['code']
    data = {
        'code': auth_code,
        'client_id': '184797883583-a5f3khiol3btdqdvnbd225cic0h8m8i1.apps.googleusercontent.com',  
        'client_secret': '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',  
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code'
    }
    response = requests.post('https://oauth2.googleapis.com/token', data=data).json()
    headers = {
            'Authorization': f'Bearer {response["access_token"]}'
        }
    user_info = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers).json()
    ## check user if exist
    # user = user_model()
    # if  user.get_user_by_google_id(user_info['sub']) == True:
    #     jwt_token = user.login_user_google(user_info['sub'])
    #     print('has')
    #     return make_response(jsonify(access_token = jwt_token), 200)
    # else: 
    #     user.register_with_google(user_info)
    #     jwt_token = user.login_user_google(user_info['sub'])
    #     print(jwt_token)
    #     return make_response(jsonify(access_token = jwt_token), 200)

    