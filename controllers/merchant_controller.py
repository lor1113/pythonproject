from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

from static.constants import colour_list, colour_dict

merchants_blueprint = Blueprint("merchants",__name__)

@merchants_blueprint.route("/merchants")
def display_merchants():
    merchants = merchant_repository.select_active()
    return render_template("merchants/index.html",merchants=merchants,colour_dict=colour_dict)

@merchants_blueprint.route("/merchants/new")
def merchant_form():
    tag_list = tag_repository.select_all()
    return render_template("merchants/new.html",tag_list=tag_list,colour_list=colour_list)

@merchants_blueprint.route("/merchants",methods=["POST"])
def new_merchant():
    name = request.form["name"]
    colour = request.form["colour"]
    tag_ids = [int(tag) for tag in request.form.getlist("tags")]
    merchant = Merchant(name,None,colour,tag_ids=tag_ids)
    merchant_repository.save_merchant(merchant)
    return redirect("/merchants")

@merchants_blueprint.route("/merchants/<id>")
def show_merchant(id):
    merchant = merchant_repository.select(id)
    transactions = transaction_repository.select_merchant(id)
    transactions.sort(key=lambda transaction: int(transaction.id))
    return render_template("merchants/show.html",merchant=merchant,colour_dict=colour_dict,transactions=transactions)

@merchants_blueprint.route("/merchants/<id>/delete")
def delete_merchant(id):
    transactions = transaction_repository.select_merchant(id)
    for transaction in transactions:
        transaction.deactivated = True
        transaction_repository.update(transaction)
    merchant = merchant_repository.select(id)
    merchant.deactivated = True
    merchant_repository.update(merchant)
    return redirect("/merchants")

@merchants_blueprint.route("/merchants/<id>/edit")
def merchant_edit_form(id):
    merchant = merchant_repository.select(id)
    tag_list = tag_repository.select_all()
    return render_template("merchants/edit.html",merchant=merchant,tag_list=tag_list,colour_list=colour_list)

@merchants_blueprint.route("/merchants/<id>",methods=["POST"])
def edit_merchant(id):
    name = request.form["name"]
    colour = request.form["colour"]
    tag_ids = [int(tag) for tag in request.form.getlist("tags")]
    merchant = Merchant(name,None,colour,tag_ids=tag_ids)
    merchant.id = id
    merchant_repository.update(merchant)
    return redirect("/merchants/" + id)