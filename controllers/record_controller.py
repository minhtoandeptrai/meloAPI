from models.record_model import record_model
from models.auth_model import auth_model
from flask import request
from app import app

#base url: http://127.0.0.1:5000

record = record_model()
auth = auth_model()

# get record
@app.route("/record")
def get_record():
    _user = request.args.get("user")
    _id = request.args.get("id")
    _cate= request.args.get("cate")
    _album = request.args.get("album")
    return record.get_record(user= _user,id=_id, cate=_cate, album=_album)

# post record
@app.route("/record/add", methods=['post'])
def add_record():
    return record.add_new_record(request)

@app.route("/record/addtoalbum", methods = ['patch'])
def add_to_album():
    return record.add_to_album(request.form)

@app.route("/record/hide", methods = ['patch'])
def hide_records():
    return record.hide_record(request.form)