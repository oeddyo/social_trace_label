from flask import render_template, request, redirect, url_for
from app import app
from annotator import Annotator
import json
import flask
import os
import pymongo

@app.route('/consent')
def consent():
    return render_template("consent.html", next="/welcome")

@app.route('/welcome')
def welcome():
    return render_template("welcome.html", next="/login") 

@app.route('/logout')
def logout():
    return """Dear participants,
    Thank you for participating in our study. Please note that some of the information in the tweets you read in this study may not be true. If you are uncomfortable with your responses to the tweets, you can withdraw your participation now and you will not be penalized in any way. 
    Please feel free to email Jin Liu at jl2523@cornell.edu, Ke Xie at kx29@cornell.edu, or Jean Marcel Dos Reis Costa at jmd487@cornell.edu, if you have any questions.

    Thanks!
    Research Team"""

@app.route('/annotate', methods = ['POST', 'GET'])
def annotate():
    user_post = flask.users[flask.session['sessionid']].get_next()
    if user_post == None:
        return flask.redirect(flask.url_for('logout'))
    
    user_dic = json.loads(user_post)
    if request.method == "POST":
        answer = flask.request.form.get("answer")
        user_dic['answer'] = answer
        user_dic['session'] = str(flask.session['sessionid'])
        
        conn = pymongo.MongoClient(host='grande.rutgers.edu')
        cursor = conn['social_trace']['annotation']
        cursor.insert({'annotation':user_dic})
        
        #db_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'db/data.json' )
        #print 'db ', db_path
        #with open(db_path, "a") as outfile:
        #    json.dump(user_dic, outfile, indent=4)

        print user_dic
    return render_template('annotate.html',next='/annotate', user_dic = user_dic)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if not flask.request.args.get('sessionid'):
        import uuid
        flask.session['sessionid'] = uuid.uuid4()
        if flask.session['sessionid'] not in flask.users:
            flask.users[flask.session['sessionid']] = Annotator()

        if request.method == 'POST':
            annotator_age = flask.request.form.get('age')
            print flask.request.form.keys()
            
            conn = pymongo.MongoClient(host='grande.rutgers.edu')
            cursor = conn['social_trace']['subject']
            
            for key in flask.request.form.keys():
                cursor.insert({"subject": str(flask.session['sessionid']), key: flask.request.form.get(key)} )
            
        return flask.redirect(flask.url_for('annotate'))

