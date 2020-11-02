from flask import Blueprint,render_template,request
from flask_login import logout_user
from cardination.main.utils import searching,worker

main = Blueprint('main',__name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html")

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@main.route("/response")
def response():
    message = request.args.get('message')
    result = searching(message)
    if result==None:
        result = worker(message)
    return render_template("answer.html",result = result)