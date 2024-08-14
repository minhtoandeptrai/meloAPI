from models.section_model import section_model
from flask import request
from app import app

#base url: http://127.0.0.1:5000


section = section_model()
# get record
@app.route("/section/danhchoban")
def get_section_danhchoban():
    return section.get_DanhChoBan()
@app.route("/section/albumnoibat")
def get_section_AlbumNoiBat():
    return section.get_AlbumNoiBat()
@app.route("/section/nguoidungnoibat")
def get_section_NguoiDungNoiBat():
    return section.get_NguoiDungNoiBat()
@app.route("/section/danhsachphatnoibat")
def get_section_DanhSanhPhatNoiBat():
    return section.get_DanhSanhPhatNoiBat()
