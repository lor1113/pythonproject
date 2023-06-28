from flask import Flask, render_template, request, redirect, url_for
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
    args = request.args
    transactions = transaction_repository.select_active()
    selected_tags = []
    if args.__contains__("filter"):
        transactions = transaction_filter(transactions,args)
        if args.__contains__("tags"):
            selected_tags = [int(x) for x in args.getlist("tags")]
        args = dict(args)
        if args["merchant"]:
            args["merchant"] = int(args["merchant"])
        if selected_tags:
            args["tags"] = selected_tags

    transactions.sort(key=lambda transaction: int(transaction.id))
    if args.__contains__("sortdir"):
        transactions = transactions_sort(transactions,args["sortdir"])
    merchant_list = merchant_repository.select_active()
    tag_list = tag_repository.select_active()
    return render_template("transactions/index.html",transactions=transactions,merchant_list=merchant_list,tag_list=tag_list,colour_dict=colour_dict,args=args)

def transaction_filter(transactions,args):
    out = []
    name = args["name"]
    merchant = args["merchant"]
    above = 0
    below = 0
    if args["above"]:
        above = int(args["above"])
    if args["below"]:
        below = int(args["below"])
    tags = []
    time_check = True
    money_check = True
    if args.__contains__("tags"):
        tags = args.getlist("tags")
    before_time = None
    if args["before_time"]:
        before_time = datetime.strptime(args["before_time"],"%Y-%m-%d")
    after_time = None
    if args["after_time"]:
        after_time = datetime.strptime(args["after_time"],"%Y-%m-%d")
    for transaction in transactions:
        if str(transaction.merchant.id) == merchant or not merchant:
            if name.lower() in transaction.name.lower() or not name:
                if any(str(x) in tags for x in transaction.tag_ids) or not tags:
                        if int(transaction.amount) > above or not above:
                            if int(transaction.amount) < below or not below:
                                if before_time:
                                    time_check = False
                                    if transaction.timestamp < before_time or not before_time:
                                        time_check = True
                                if after_time:
                                    time_check = False
                                    if transaction.timestamp > after_time or not after_time:
                                        time_check = True
                                if time_check:
                                    out.append(transaction)
    return out

def transactions_sort(transactions,sortdir):
    if sortdir == "timeup":
        transactions.sort(key=lambda transaction: transaction.timestamp)
    elif sortdir == "timedown":
        transactions.sort(reverse=True,key=lambda transaction: transaction.timestamp)
    elif sortdir == "moneyup":
        transactions.sort(key=lambda transaction: int(transaction.amount))
    elif sortdir == "moneydown":
        transactions.sort(reverse=True,key=lambda transaction: int(transaction.amount))
    return transactions

@transactions_blueprint.route("/transactions/new")
def transaction_form():
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%dT%H:%M")
    merchant_list = merchant_repository.select_active()
    tag_list = tag_repository.select_active()
    return render_template("transactions/new.html",tag_list=tag_list,merchant_list=merchant_list,date_string=date_string)

@transactions_blueprint.route("/transactions",methods=["POST"])
def new_transaction():
    name = request.form["name"]
    amount = request.form["amount"]
    timestamp = request.form["time"]
    merchant_id = request.form["merchant"]
    merchant = merchant_repository.select(merchant_id)
    tag_ids = [int(tag) for tag in request.form.getlist("tags")]
    tag_ids.extend(merchant.tag_ids)
    tag_ids = list(set(tag_ids))
    transaction = Transaction(name,amount,None,merchant,timestamp,tag_ids=tag_ids)
    transaction_repository.save_transaction(transaction)
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/<id>/edit")
def transaction_edit_form(id):
    transaction = transaction_repository.select(id)
    merchant_list = merchant_repository.select_active()
    tag_list = tag_repository.select_active()
    date_string = transaction.timestamp.strftime("%Y-%m-%dT%H:%M")
    return render_template("transactions/edit.html",transaction=transaction,tag_list=tag_list,merchant_list=merchant_list,date_string = date_string)

@transactions_blueprint.route("/transactions/<id>")
def show_transaction(id):
    transaction = transaction_repository.select(id)
    return render_template("transactions/show.html",transaction=transaction,colour_dict=colour_dict)

@transactions_blueprint.route("/transactions/<id>",methods=["POST"])
def edit_transaction(id):
    name = request.form["name"]
    amount = request.form["amount"]
    timestamp = request.form["time"]
    merchant_id = request.form["merchant"]
    merchant = merchant_repository.select(merchant_id)
    tag_ids = [int(tag) for tag in request.form.getlist("tags")]
    transaction = Transaction(name,amount,None,merchant,timestamp,tag_ids=tag_ids)
    transaction.id = id
    transaction_repository.update(transaction)
    return redirect("/transactions/"+id)

@transactions_blueprint.route("/transactions/<id>/delete")
def delete_transaction(id):
    transaction_repository.select_active()
    transaction = transaction_repository.select(id)
    transaction.deactivated = True
    transaction_repository.update(transaction)
    transaction_repository.select_active()
    return redirect("/transactions")