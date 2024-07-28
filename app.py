from flask import Flask
from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'MeloSpace API'

import controllers.song_controller