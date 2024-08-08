from models.user_model import user_model
from models.auth_model import auth_model
from flask import request
from app import app
#base url: http://127.0.0.1:5000
user = user_model()
auth = auth_model()


@app.route('/user')
def get_user_by_id():
    id = request.args.get('id')
    print(id)
    return user.get_user_by_id(id)

@app.route('/user/login',  methods=['post'])
def login_user():
    return user.login_user(request.form)

@app.route('/user/register', methods=['post'])
def register():
    return user.register(request.form)

@app.route('/user/update', methods=['patch'])
def update_user():
    return user.update_information(request.form)