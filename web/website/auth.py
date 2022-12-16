from flask import Blueprint, render_template, request, flash

# it has a bunch of root
auth = Blueprint('auth', __name__)


@auth.route('/home', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "elektro@elektro.upnvj" and password == "elektro":
            return render_template("home.html")
        else:
            if len(username) != 0:
                flash("Cant Login, wrong Account", category="error")
                print("gagagl")


@auth.route('/signup')
def signup():
    return render_template("sign-up.html")
