from models.section_model import section_model
from flask import request
from app import app

#base url: http://127.0.0.1:5000

section = section_model()
# get record
@app.route("/section")
def get_section():
    return section.get_all_section()

@app.route("/section/list")
def get_list():
    id = request.args.get('id')
    return section.get_section_item(id)
