from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, current_user, logout_user
from wtform_fields import *
from models import *
from flask_mail import  Mail
import stripe
import os


app = Flask(__name__)
app.secret_key =  "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"
app.config['SQLALCHEMY_DATABASE_URI']="postgres://zdnflzvvlqpfnh:969ea6081a951573fea186d2529458d67b47aa4c74aaa6ffe115c4e67edb57d9@ec2-3-224-38-18.compute-1.amazonaws.com:5432/d6875qun2srg99"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(MAIL_SERVER="smtp.gmail.com",
MAIL_PORT="465",
MAIL_USE_SSL ="True",
MAIL_USERNAME="digitaltrends86@gmail.com",
MAIL_PASSWORD="mohit0953")
mail = Mail(app)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
	return User.query.filter_by(id=id).first()
	
@app.route("/", methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        email = reg_form.email.data
        
        hashed_pswd = pbkdf2_sha256.hash(password)
        user = User(username=username, password=hashed_pswd, email = email)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
    	user_object = User.query.filter_by(username = login_form.username.data).first()
    	login_user(user_object)
    	return redirect(url_for("home"))

    return render_template("login.html", form=login_form)
 
@app.route("/home", methods = ["GET","POST"])
def home():
	if not current_user.is_authenticated:
		flash("Please Login to continue", "danger")
		return redirect(url_for("login"))
	return render_template("page.html", username = current_user.username)
	
@app.route("/logout", methods = ["GET"])
def logout():
	logout_user()
	flash("You have been Logged out successfully", "success")
	return redirect(url_for("login"))

@app.route("/about", methods=["GET"])
def about():
	if not current_user.is_authenticated:
		flash("Please Login to continue", "danger")
		return redirect(url_for("login"))
	return render_template("about.html", username = current_user.username)

@app.route("/order", methods=["GET", "POST"])
def order():
	order_form = Order()
	if not current_user.is_authenticated:
		flash("Please Login to continue", "danger")
		return redirect(url_for("login"))
	if order_form.validate_on_submit():
		name = order_form.name.data
		email = order_form.email.data
		message = order_form.message.data
		data = Orderf(name = name, email= email, message = message)
		db.session.add(data)
		db.session.commit()
		mail.send_message("New mesage from"+" "+current_user.username, sender = email, recipients = ["digitaltrends86@gmail.com"], body = name + "\n" + "sender: " + email + "\n" + message)
		flash("Order placed successfully", "success")
	return render_template("order.html", form=order_form, username = current_user.username)
	
if __name__ == "__main__":
    app.run(debug=True)
