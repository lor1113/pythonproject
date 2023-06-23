from flask import Flask, render_template, request, redirect
from flask import Blueprint

import repositories.transaction_repository as transaction_repository

transactions_blueprint = Blueprint("transactions",__name__)

@transactions_blueprint.route("/transactions")
def display_transactions():
    transactions = transaction_repository.select_all()
    return render_template("transactions/index.html",transactions=transactions)

@transactions_blueprint.route("/transactions/new")
def new_transaction():
    return render_template("transactions/form.html")