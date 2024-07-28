from flask import Flask
from azure.storage import blob
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'MeloSpace API'
