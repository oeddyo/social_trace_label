from flask import Flask
import flask
app = Flask(__name__)
app.secret_key = 'secret key'
from app import views
flask.users = {}

