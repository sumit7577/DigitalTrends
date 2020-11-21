from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(),unique = True, nullable = False)
    password = db.Column(db.String(), nullable=False)

class Orderf(db.Model):
	
	__tablename__ = "orders"
	sno = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), unique=False, nullable=False)
	email = db.Column(db.String(), unique = False,nullable= False)
	message = db.Column(db.String(120),unique = False, nullable = False)

