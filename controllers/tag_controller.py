from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.tag import Tag

import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

from static.constants import colour_list,colour_dict

tags_blueprint = Blueprint("tags",__name__)

@tags_blueprint.route("/tags")
def display_tags():
    print("display tags")
    tags = tag_repository.select_active()
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

@tags_blueprint.route("/tags/<id>")
def show_tag(id):
    tag = tag_repository.select(id)
    transactions = transaction_repository.select_tag(id)
    transactions.sort(key=lambda transaction: int(transaction.id))
    return render_template("tags/show.html",tag=tag,colour_dict=colour_dict,transactions=transactions)

@tags_blueprint.route("/tags/<id>/edit")
def tag_edit_form(id):
    tag = tag_repository.select(id)
    return render_template("tags/edit.html",tag=tag,colour_list = colour_list)

@tags_blueprint.route("/tags/<id>",methods=["POST"])
def edit_tag(id):
    name = request.form["name"]
    colour = request.form["colour"]
    tag = Tag(name,colour)
    tag.id = id
    tag_repository.update(tag)
    return redirect("/tags/"+id)

@tags_blueprint.route("/tags/<id>/delete")
def delete_tag(id):
    tag = tag_repository.select(id)
    tag.deactivated = True
    tag_repository.update(tag)
    return redirect("/tags")
