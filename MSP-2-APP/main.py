import helper
from flask import Flask, request, Response, render_template, redirect
import json
import os.path
import requests
from pprint import pprint
import time
import urllib

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
        return Response("Votre commentaire a été enregistré.")    

    
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
        return Response("Hello ! Fuck you !" + moderation_api(comment))    

    
    req_data = request.get_json()
    comment = req_data['comment']

    res_data = helper.add_to_list(comment)

    if res_data is None:
        response = Response("{'error': 'comment not added - " + comment + "'}", status=400 , mimetype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')

    return render_template("index.html")


# moderation api
def moderation_api(comment):

    # Request headers
    headers = {
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': 'db8e4602d7df4f6aa85d537558c3a63a'
    }

    # Request parameters
    params = ({'classify': 'True'})

    body = [{'text' :comment}]
    # body = [{'text' :'Putain de merde'}]
    url = 'https://francecentral.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen?classify=True'
    r = requests.post(url, json = body, params = params,headers= headers )
    # print(r.status_code, r.reason)
    # print(r.text)
    json_data = json.loads(r.text)
    # pprint(json_data)
    # pprint(json_data['Classification'])

    return r.text