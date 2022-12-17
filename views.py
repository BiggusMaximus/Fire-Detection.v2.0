from flask import Blueprint, render_template

# it has a bunch of root
views = Blueprint('views', __name__)


@views.route('/')
def login():
    return render_template("login.html")
