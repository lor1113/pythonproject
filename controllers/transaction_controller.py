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
    print("display transactions")
    args = request.args
    transactions = transaction_repository.select_all()
    if args.__contains__("filter"):
        transactions = transaction_filter(transactions,args)
        args = dict(args)
        if args["merchant"]:
            args["merchant"] = int(args["merchant"])
        if args.__contains__("tags"):
            args["tags"] = [int(x) for x in args["tags"]]
    merchant_list = merchant_repository.select_all()
    tag_list = tag_repository.select_all()
    tag_dict = {tag.id:tag for tag in tag_list}
    return render_template("transactions/index.html",transactions=transactions,merchant_list=merchant_list,tag_list=tag_list,tag_dict=tag_dict,colour_dict = colour_dict,args=args)

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
            if name in transaction.name or not name:
                if any(str(x) in tags for x in transaction.tags) or not tags:
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
    transactions.sort(key=lambda transaction: int(transaction.id))
    if args.__contains__("sortdir"):
        if args["sortdir"] == "timeup":
            transactions.sort(key=lambda transaction: transaction.timestamp)
        elif args["sortdir"] == "timedown":
            transactions.sort(reverse=True,key=lambda transaction: transaction.timestamp)
        elif args["sortdir"] == "moneyup":
            transactions.sort(key=lambda transaction: int(transaction.amount))
        elif args["sortdir"] == "moneydown":
            transactions.sort(reverse=True,key=lambda transaction: int(transaction.amount))
    print([transaction.id for transaction in transactions])
    return out

@transactions_blueprint.route("/transactions/new")
def transaction_form():
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%dT%H:%M")
    merchant_list = merchant_repository.select_all()
    tag_list = tag_repository.select_all()
    return render_template("transactions/new.html",tag_list=tag_list,merchant_list=merchant_list,date_string=date_string)

@transactions_blueprint.route("/transactions",methods=["POST"])
def new_transaction():
    print("new transaction")
    name = request.form["name"]
    amount = request.form["amount"]
    tags = [int(tag) for tag in request.form.getlist("tags")]
    merchant_id = request.form["merchant"]
    merchant = merchant_repository.select(merchant_id)
    tags.extend(merchant.auto_tags)
    tags = list(set(tags))
    timestamp = request.form["time"]
    transaction = Transaction(name,amount,tags,merchant_id,timestamp)
    transaction_repository.save_transaction(transaction)
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/<id>/edit")
def transaction_edit_form(id):
    transaction = transaction_repository.select(id)
    merchant_list = merchant_repository.select_all()
    tag_list = tag_repository.select_all()
    date_string = transaction.timestamp.strftime("%Y-%m-%dT%H:%M")
    return render_template("transactions/edit.html",transaction=transaction,tag_list=tag_list,merchant_list=merchant_list,date_string = date_string)

@transactions_blueprint.route("/transactions/<id>")
def show_transaction(id):
    transaction = transaction_repository.select(id)
    return render_template("transactions/show.html",transaction=transaction)

@transactions_blueprint.route("/transactions/<id>",methods=["POST"])
def edit_transaction(id):
    name = request.form["name"]
    amount = request.form["amount"]
    tags = [int(tag) for tag in request.form.getlist("tags")]
    merchant_id = request.form["merchant"]
    merchant = merchant_repository.select(merchant_id)
    tags.extend(merchant.auto_tags)
    tags = list(set(tags))
    timestamp = request.form["time"]
    transaction = Transaction(name,amount,tags,merchant_id,timestamp,id)
    transaction_repository.update(transaction)
    return redirect("/transactions")