from flask import render_template, request, redirect, url_for
from app import app
from annotator import Annotator
import json
import flask
import os

@app.route('/welcome')
def welcome():
    return render_template("welcome.html", next="/login") 

@app.route('/logout')
def logout():
    return "Thanks. Bye..."

@app.route('/annotate', methods = ['POST', 'GET'])
def annotate():
    user_post = flask.users[flask.session['sessionid']].get_next()
    user_dic = json.loads(user_post)
    if user_post == None:
        return flask.redirect(flask.url_for('logout'))
    
    if request.method == "POST":
        answer = flask.request.form.get("answer")
        user_dic['answer'] = answer
        user_dic['session'] = str(flask.session['sessionid'])
         
        db_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'db/data.json' )
        print 'db ', db_path
        with open(db_path, "a") as outfile:
            json.dump(user_dic, outfile, indent=4)

        print user_dic
    return render_template('annotate.html', user_dic = user_dic)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if not flask.request.args.get('sessionid'):
        import uuid
        flask.session['sessionid'] = uuid.uuid4()
        if flask.session['sessionid'] not in flask.users:
            flask.users[flask.session['sessionid']] = Annotator()

        if request.method == 'POST':
            annotator_age = flask.request.form.get('age')
            print 'age = ', annotator_age
        return flask.redirect(flask.url_for('annotate'))
