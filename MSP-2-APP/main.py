# coding: utf-8
import helper
from flask import Flask, request, Response, render_template, redirect
import json
import os.path
import requests
from pprint import pprint
import time
import urllib
import sys
from queries.moderation import moderation_api
import config
# reload(sys)
# sys.setdefaultencoding('UTF8')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/comment/new', methods=['POST'])
def add_comment():
    # Get comment from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        comment = req["comment"]
        return Response("ok")    

    req_data = request.get_json()
    comment = req_data['comment']

    res_data = helper.add_to_list(comment)

    if res_data is None:
        response = Response("{'error': 'comment not added - " + comment + "'}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')

    return render_template("index.html")



@app.route('/comment/moderation', methods=['POST'])
def moderation():
    # Get comment from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        comment = req["comment"]
        result_moderation = moderation_api(comment)

        # Traitement commentaire
        if result_moderation["Terms"] == None :
           texte = "Votre commentaire a été enregistré"
           res_data = helper.add_to_list(comment)
        elif  len(result_moderation["Terms"]) == 1:
            texte = "Votre commentaire a ete modéré à cause du mot {}".format(result_moderation["Terms"][0]['Term'])
        elif len(result_moderation["Terms"]) > 1:
            texte = "Votre commentaire a été supprimé !!"

        # Render template
        return render_template("index.html", commentaire=comment, message=texte)

@app.route('/base', methods=['POST'])
def base():
    # res = helper.get_list()
    # response = Response(helper.get_list(), status=400 , mimetype='application/json')
    # # response = Response(res, mimetype='application/json')
    # # return render_template("index.html", liste=helper.get_list())
    # # return render_template("index.html")
    # return response

    # conn = sqlite3.connect(DB_PATH)
    # c = conn.cursor()
    # posts = conn.execute('SELECT * FROM comments').fetchall()
    # conn.close()
    # return render_template('index.html', posts=posts)
    return render_template('index.html')


