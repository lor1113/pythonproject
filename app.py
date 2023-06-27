from flask import Flask, render_template, request
from werkzeug.urls import url_encode

from controllers.tag_controller import tags_blueprint
from controllers.merchant_controller import merchants_blueprint
from controllers.transaction_controller import transactions_blueprint

app = Flask(__name__)

app.register_blueprint(transactions_blueprint)
app.register_blueprint(merchants_blueprint)
app.register_blueprint(tags_blueprint)

@app.template_global()
def sort_url(sortdir):
    args = dict(request.args)
    args["sortdir"] = sortdir
    return '{}?{}'.format(request.path, url_encode(args))

@app.route('/')
def home():
    print("Home")
    return render_template('index.html')

@app.route('/testing')
def testing():
    print("testing")
    return render_template("base.html")

if __name__ == '__main__':
    app.run(debug=True)