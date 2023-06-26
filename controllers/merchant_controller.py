from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

from static.constants import colour_list

merchants_blueprint = Blueprint("merchants",__name__)

@merchants_blueprint.route("/merchants")
def display_transactions():
    merchants = merchant_repository.select_all()
    return render_template("merchants/index.html",merchants=merchants)

@merchants_blueprint.route("/merchants/new")
def merchant_form():
    tag_list = tag_repository.select_all()
    print(tag_list)
    return render_template("merchants/new.html",tag_list=tag_list,colour_list=colour_list)

@merchants_blueprint.route("/merchants",methods=["POST"])
def new_merchant():
    print(request.form)
    name = request.form["name"]
    colour = request.form["colour"]
    auto_tags = [int(tag) for tag in request.form.getlist("tags")]
    print(auto_tags)
    merchant = Merchant(name,auto_tags,colour)
    merchant_repository.save_merchant(merchant)
    return redirect("/merchants")