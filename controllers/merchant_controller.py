from flask import Flask, render_template, request, redirect
from flask import Blueprint

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

merchants_blueprint = Blueprint("merchants",__name__)

@merchants_blueprint.route("/merchants")
def display_transactions():
    merchants = merchant_repository.select_all()
    return render_template("merchants/index.html",merchants=merchants)

@merchants_blueprint.route("/merchants/new")
def merchant_form():
    tags = tag_repository.select_all()
    return render_template("merchants/new.html",tags=tags)