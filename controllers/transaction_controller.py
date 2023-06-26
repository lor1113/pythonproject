from flask import Flask, render_template, request, redirect
from flask import Blueprint

from datetime import datetime

import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

from models.transaction import Transaction

from static.constants import colour_list,colour_dict

transactions_blueprint = Blueprint("transactions",__name__)

@transactions_blueprint.route("/transactions")
def display_transactions():
    transactions = transaction_repository.select_all()
    merchants = merchant_repository.select_all()
    tag_list = tag_repository.select_all()
    tag_dict = {tag.id:tag for tag in tag_list}
    return render_template("transactions/index.html",transactions=transactions,merchants=merchants,tag_dict=tag_dict,colour_dict = colour_dict)

@transactions_blueprint.route("/transactions/new")
def transaction_form():
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%dT%H:%M")
    merchant_list = merchant_repository.select_all()
    tag_list = tag_repository.select_all()
    return render_template("transactions/new.html",tag_list=tag_list,merchant_list=merchant_list,date_string=date_string)

@transactions_blueprint.route("/transactions",methods=["POST"])
def new_transaction():
    name = request.form["name"]
    amount = request.form["amount"]
    tags = [int(tag) for tag in request.form.getlist("tags")]
    merchant_id = request.form["merchant"]
    merchant = merchant_repository.select(merchant_id)
    tags.extend(merchant.auto_tags)
    tags = list(set(tags))
    print(tags)
    timestamp = request.form["time"]
    transaction = Transaction(name,amount,tags,merchant_id,timestamp)
    transaction_repository.save_transaction(transaction)
    return redirect("/transactions")