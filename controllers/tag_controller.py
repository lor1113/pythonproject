from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.tag import Tag

import repositories.tag_repository as tag_repository

from static.constants import colour_list,colour_dict

tags_blueprint = Blueprint("tags",__name__)

@tags_blueprint.route("/tags")
def display_tags():
    print("display tags")
    tags = tag_repository.select_all()
    return render_template("tags/index.html",tags=tags,colour_dict=colour_dict)

@tags_blueprint.route("/tags/new")
def tag_form():
    return render_template("tags/new.html", colour_list = colour_list)

@tags_blueprint.route("/tags",methods=["POST"])
def new_tag():
    name = request.form["name"]
    colour = request.form["colour"]
    tag = Tag(name,colour)
    tag_repository.save_tag(tag)
    return redirect("/tags")