from flask import Flask, render_template, request, redirect
from flask import Blueprint

import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

transactions_blueprint = Blueprint("transactions",__name__)

@transactions_blueprint.route("/transactions")
def display_transactions():
    transactions = transaction_repository.select_all()
    merchants = merchant_repository.select_all()
    tag_list = tag_repository.select_all()
    return render_template("transactions/index.html",transactions=transactions,merchants=merchants,tag_list=tag_list)

@transactions_blueprint.route("/transactions/new")
def new_transaction():
    return render_template("transactions/new.html")