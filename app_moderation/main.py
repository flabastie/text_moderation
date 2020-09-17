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
    # Récup liste commentaires depuis bd
    res = helper.get_list()
    return render_template("index.html", data=res)

@app.route('/comment/moderation', methods=['POST'])
def moderation():
    # Get comment from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        comment = req["comment"]
        result_moderation = moderation_api(comment)

        # Traitement commentaire
        if len(comment) != 0:
            if result_moderation["Terms"] == None :
                texte = "Bravo! Votre commentaire a été enregistré"
                # Enregistrement du commentaire en bd
                helper.add_to_list(comment)
            elif  len(result_moderation["Terms"]) == 1:
                texte = "Votre commentaire a été modéré à cause du mot {}".format(result_moderation["Terms"][0]['Term'])
            elif len(result_moderation["Terms"]) > 1:
                texte = "Désolé, votre commentaire a été modéré pour cause de vulgarité !!"
        else:
            texte = "Aucun commentaire saisi."

        # Récup liste commentaires depuis bd
        res = helper.get_list()

        # Render template
        return render_template("index.html", message=texte, data=res)


@app.route('/comment/listmoderation', methods=['POST'])
def listmoderation():
    # Get comment from the POST body
    if request.method == "POST":
        req = request.form.to_dict()
        comment = req["comment"]
        comment_list = list(comment.split(" ")) 
        comment_list = [x.lower() for x in comment_list]

        # Recup forbidden words
        f = open("app_moderation/checklist.txt", "r")
        forbidden_list = f.read()
        forbidden_list = list(forbidden_list.split("\n"))
        forbidden_list = [x.lower() for x in forbidden_list]

        # lists compare intersection
        inter_list = list(set(comment_list) & set(forbidden_list)) 
         
        # Traitement commentaire
        if len(comment) != 0:
            if len(inter_list) == 0 :
                texte = "Bravo! Votre commentaire a été enregistré"
                # Enregistrement du commentaire en bd
                helper.add_to_list(comment)
            elif  len(inter_list) == 1:
                texte = "Votre commentaire a été modéré à cause du mot {}".format(inter_list[0])
            elif len(inter_list) > 1:
                forbidden_words = ', '.join(inter_list)
                texte = "Désolé, votre commentaire a été modéré pour cause de vulgarité !! ({})".format(forbidden_words)
        else:
            texte = "Aucun commentaire saisi."

        # Récup liste commentaires depuis bd
        res = helper.get_list()

        # Render template
        return render_template("index.html", message=texte, data=res)


