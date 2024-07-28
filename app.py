from flask import Flask
import controllers.song_controller

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'MeloSpace API'